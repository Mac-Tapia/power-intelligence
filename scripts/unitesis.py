"""UNITESIS single entry point: studies, scenarios, alternatives, evidence, datasets, server.

  python scripts/unitesis.py study --input fixtures/networks/radial_feeder_6bus.json \
      --output local-data/evidence/base.json
  python scripts/unitesis.py new-load --input ... --output ... --load-id NL1 --bus B3 \
      --p-mw 0.5 --q-mvar 0.2
  python scripts/unitesis.py alternatives --input ... --output ... --line L13 \
      --catalog config/catalogs/conductors/aaac6201_nexans_reference.json \
      --basis fixtures/economics/conductor_alternatives_synthetic.json \
      --temperature-c 75 --gmd-m 1.2
  python scripts/unitesis.py import-cyme --case pe-ica-electrodunas --network RED.txt \
      --loads CARGA.txt --equipment BD_Equipo.txt --out-dir local-data/networks/eldu
  python scripts/unitesis.py verify-evidence local-data/evidence/base.json
  python scripts/unitesis.py dataset --input fixtures/timeseries/synthetic_feeder_load.csv \
      --output local-data/datasets/s --target p_mw --freq 15min
  python scripts/unitesis.py serve [--port 8000] [--db local-data/unitesis.sqlite]

Exit codes: 0 ok | 2 invalid/quarantined input | 3 reference engine or runtime unavailable |
4 not converged | 5 comparison failed | 6 evidence corrupt.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
for _src in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(_src))
sys.path.insert(0, str(ROOT / "apps/control-api/src"))

from unitesis_adapters.neutral_json import IngestionError  # noqa: E402
from unitesis_evidence.store import EvidenceError, read_evidence  # noqa: E402

EXIT_OK, EXIT_INVALID, EXIT_UNAVAILABLE, EXIT_NOT_CONVERGED = 0, 2, 3, 4
EXIT_COMPARISON, EXIT_EVIDENCE = 5, 6


def _print(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_study(a: argparse.Namespace) -> int:
    from unitesis_application.study import engine_by_name, run_study

    result = run_study(a.input, a.output, scenario_id=a.scenario,
                       candidate=engine_by_name(a.engine))
    comparison = result["comparison"]
    _print({"status": result["status"], "snapshot_sha256": result["snapshot_sha256"],
            "comparison": comparison.get("status"),
            "max_differences": comparison.get("max_differences"),
            "evidence": str(Path(a.output).resolve()), "technical_acceptance": False})
    if result["status"] != "computed":
        return EXIT_NOT_CONVERGED
    return {"passed": EXIT_OK, "unavailable": EXIT_UNAVAILABLE}.get(comparison["status"],
                                                                    EXIT_COMPARISON)


def cmd_new_load(a: argparse.Namespace) -> int:
    from unitesis_application.study import engine_by_name, run_new_load_study

    result = run_new_load_study(a.input, a.output, load_id=a.load_id, bus=a.bus, p_mw=a.p_mw,
                                q_mvar=a.q_mvar, v_min_pu=a.v_min_pu,
                                max_loading_percent=a.max_loading_percent,
                                candidate=engine_by_name(a.engine))
    _print({"screening": result["screening"], "violations": result["violations"],
            "before": result["before"]["summary"], "after": result["after"]["summary"],
            "comparison_after": result["after"]["comparison"]["status"],
            "evidence": str(Path(a.output).resolve()), "technical_acceptance": False})
    return EXIT_NOT_CONVERGED if result["screening"] == "not_computed" else EXIT_OK


def cmd_alternatives(a: argparse.Namespace) -> int:
    from unitesis_application.alternatives import run_conductor_alternatives

    result = run_conductor_alternatives(
        a.input, a.output, line_id=a.line, catalog_path=a.catalog, basis_path=a.basis,
        operating_temperature_c=a.temperature_c, phase_gmd_m=a.gmd_m, v_min_pu=a.v_min_pu,
        max_loading_percent=a.max_loading_percent)
    _print({"line_id": result["line_id"], "recommended": result["recommended"],
            "smallest_feasible_section": result["smallest_feasible_section"],
            "ranking": result["ranking"],
            "currency": result["economic_basis"]["currency"],
            "evidence": str(Path(a.output).resolve()), "status": result["status"]})
    return EXIT_OK


def cmd_import_cyme(a: argparse.Namespace) -> int:
    from unitesis_application.network_import import import_cyme_export
    from unitesis_config import load_case

    case = load_case(ROOT / "config/cases" / f"{a.case}.json")
    report = import_cyme_export(case, a.network, a.loads, a.equipment, a.out_dir,
                                allow_positive_sequence=a.allow_positive_sequence or None)
    _print({"case_id": report["case_id"], "summary": report["summary"],
            "rules": report["rules"], "report": str(Path(a.out_dir).resolve() /
                                                    "import_report.json")})
    return EXIT_OK if report["summary"].get("model_validated") else EXIT_INVALID


def cmd_build_pf_dataset(a: argparse.Namespace) -> int:
    from unitesis_application.pf_dataset import build_pf_dataset
    from unitesis_config import load_case
    from unitesis_sciml.pf_scenarios import ScenarioSpec

    case = load_case(ROOT / "config/cases" / f"{a.case}.json")
    spec = ScenarioSpec(a.scenarios, a.u_min, a.u_max, a.sigma, a.seed,
                        contrast_fraction=a.contrast_fraction)
    m = build_pf_dataset(case, a.networks_dir, a.out_dir, spec, limit_feeders=a.limit_feeders)
    _print({"dataset_id": m["dataset_id"], "totals": m["totals"],
            "split_counts": m["split_counts"], "max_label_residual_pu": m["max_label_residual_pu"],
            "manifest": str(Path(a.out_dir).resolve() / "manifest.json")})
    contrast_ok = m["totals"]["contrast_failed"] == 0
    return EXIT_OK if m["totals"]["kept"] and contrast_ok else EXIT_COMPARISON


def cmd_eval_pf_baseline(a: argparse.Namespace) -> int:
    from unitesis_application.pf_baselines import evaluate_baseline

    r = evaluate_baseline(a.networks_dir, a.dataset_dir, a.output, split=a.split,
                          v_min_pu=a.v_min_pu)
    _print({"surrogate": r["surrogate"], "split": r["split"], "feeders": r["feeders"],
            "overall": r["overall"], "evidence": str(Path(a.output).resolve())})
    return EXIT_OK


def cmd_verify(a: argparse.Namespace) -> int:
    payload = read_evidence(a.evidence)
    _print({"status": "reread_verified", "schema": payload.get("schema"),
            "snapshot_sha256": payload.get("snapshot_sha256"),
            "technical_acceptance": payload.get("technical_acceptance")})
    return EXIT_OK


def cmd_dataset(a: argparse.Namespace) -> int:
    from unitesis_application.datasets import build_forecast_dataset
    from unitesis_sciml.datasets import DatasetError, DatasetSpec

    spec = DatasetSpec(a.timestamp, a.target, a.freq, horizon_steps=a.horizon,
                       lags=tuple(int(x) for x in a.lags.split(",")),
                       seasonal_lag=a.seasonal_lag)
    try:
        manifest = build_forecast_dataset(a.input, a.output, spec)
    except DatasetError as error:
        raise ValueError(str(error)) from error
    _print({"dataset_sha256": manifest["dataset_sha256"], "quality": manifest["quality"],
            "splits": {k: v["rows"] for k, v in manifest["splits"].items()},
            "output": str(Path(a.output).resolve())})
    return EXIT_OK


def _serve_stdlib(app: Any, host: str, port: int) -> None:
    """Local-only fallback when uvicorn is absent: stdlib HTTP server bridged in-process
    to the ASGI app. Single-threaded; background jobs finish before the response returns."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    from fastapi.testclient import TestClient

    client = TestClient(app, raise_server_exceptions=False)

    class Bridge(BaseHTTPRequestHandler):
        def _forward(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else None
            headers = {k: v for k, v in self.headers.items() if k.lower() != "host"}
            resp = client.request(self.command, self.path, content=body, headers=headers)
            self.send_response(resp.status_code)
            for key, value in resp.headers.items():
                if key.lower() not in ("content-length", "transfer-encoding", "connection"):
                    self.send_header(key, value)
            self.send_header("Content-Length", str(len(resp.content)))
            self.end_headers()
            self.wfile.write(resp.content)

        do_GET = do_POST = do_PUT = do_DELETE = _forward

        def log_message(self, fmt: str, *args: Any) -> None:
            sys.stderr.write(f"{self.command} {self.path} -> {args[1] if len(args) > 1 else ''}\n")

    server = ThreadingHTTPServer((host, port), Bridge)
    server.daemon_threads = True
    print(f"UNITESIS workstation (stdlib bridge, local only): http://{host}:{port}/")
    server.serve_forever()


def cmd_serve(a: argparse.Namespace) -> int:
    if a.host not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError("control-api has no authentication yet; bind to localhost only")
    os.environ["UNITESIS_LOCAL_ONLY"] = "1"
    try:
        from unitesis_api.main import create_app
    except ImportError as error:
        print(json.dumps({"status": "unavailable", "reason": str(error)}), file=sys.stderr)
        return EXIT_UNAVAILABLE
    app = create_app(a.db)
    try:
        import uvicorn
    except ImportError:
        _serve_stdlib(app, a.host, a.port)
        return EXIT_OK
    print(f"UNITESIS workstation: http://{a.host}:{a.port}/")
    uvicorn.run(app, host=a.host, port=a.port)
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="unitesis", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    def io(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--input", type=Path, required=True)
        sp.add_argument("--output", type=Path, required=True)

    def engine(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--engine", choices=("nr", "bfs"), default="nr",
                        help="own engine: nr = Newton-Raphson (radial/meshed), bfs = radial sweep")

    def criteria(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--v-min-pu", type=float, default=0.95)
        sp.add_argument("--max-loading-percent", type=float, default=100.0)

    s = sub.add_parser("study", help="power flow + independent comparison + evidence")
    io(s)
    s.add_argument("--scenario", default="base")
    engine(s)
    s.set_defaults(func=cmd_study)

    s = sub.add_parser("new-load", help="new customer connection on a cloned scenario")
    io(s)
    s.add_argument("--load-id", required=True)
    s.add_argument("--bus", required=True)
    s.add_argument("--p-mw", type=float, required=True)
    s.add_argument("--q-mvar", type=float, required=True)
    engine(s)
    criteria(s)
    s.set_defaults(func=cmd_new_load)

    s = sub.add_parser("alternatives", help="conductor alternatives with NPV ranking")
    io(s)
    s.add_argument("--line", required=True)
    s.add_argument("--catalog", type=Path, required=True)
    s.add_argument("--basis", type=Path, required=True, help="explicit economic basis JSON")
    s.add_argument("--temperature-c", type=float, required=True)
    s.add_argument("--gmd-m", type=float, required=True)
    criteria(s)
    s.set_defaults(func=cmd_alternatives)

    s = sub.add_parser("import-cyme", help="real network CYME ASCII export -> feeder snapshots")
    s.add_argument("--case", required=True, help="application case id (config/cases)")
    s.add_argument("--network", type=Path, required=True, help="RED_*.txt")
    s.add_argument("--loads", type=Path, required=True, help="CARGA_*.txt")
    s.add_argument("--equipment", type=Path, required=True, help="BD_Equipo*.txt")
    s.add_argument("--out-dir", type=Path, required=True)
    s.add_argument("--allow-positive-sequence", action="store_true",
                   help="import non three-phase feeders as a declared approximation")
    s.set_defaults(func=cmd_import_cyme)

    s = sub.add_parser("build-pf-dataset", help="labelled power-flow scenarios (spec 006)")
    s.add_argument("--case", required=True)
    s.add_argument("--networks-dir", type=Path, required=True, help="import-cyme output")
    s.add_argument("--out-dir", type=Path, required=True)
    s.add_argument("--scenarios", type=int, required=True, help="scenarios per feeder")
    s.add_argument("--u-min", type=float, required=True, help="min utilisation of conn. kVA")
    s.add_argument("--u-max", type=float, required=True, help="max utilisation of conn. kVA")
    s.add_argument("--sigma", type=float, required=True, help="per-load lognormal sigma")
    s.add_argument("--seed", type=int, required=True)
    s.add_argument("--contrast-fraction", type=float, default=0.1)
    s.add_argument("--limit-feeders", type=int)
    s.set_defaults(func=cmd_build_pf_dataset)

    s = sub.add_parser("eval-pf-baseline", help="score the physics baseline (AC-006-06)")
    s.add_argument("--networks-dir", type=Path, required=True)
    s.add_argument("--dataset-dir", type=Path, required=True)
    s.add_argument("--output", type=Path, required=True)
    s.add_argument("--split", choices=("train", "valid", "test"), default="test")
    s.add_argument("--v-min-pu", type=float, default=0.95)
    s.set_defaults(func=cmd_eval_pf_baseline)

    s = sub.add_parser("verify-evidence", help="re-read evidence and check its digest")
    s.add_argument("evidence", type=Path)
    s.set_defaults(func=cmd_verify)

    s = sub.add_parser("dataset", help="supervised forecasting dataset from a CSV series")
    io(s)
    s.add_argument("--timestamp", default="timestamp")
    s.add_argument("--target", required=True)
    s.add_argument("--freq", required=True)
    s.add_argument("--horizon", type=int, default=1)
    s.add_argument("--lags", default="1,2,3,4,96,672")
    s.add_argument("--seasonal-lag", type=int, default=672)
    s.set_defaults(func=cmd_dataset)

    s = sub.add_parser("serve", help="control-api + workstation UI on localhost")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8000)
    s.add_argument("--db", default=str(ROOT / "local-data/unitesis.sqlite"))
    s.set_defaults(func=cmd_serve)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except EvidenceError as error:
        print(json.dumps({"status": "evidence_failed", "reason": str(error)}), file=sys.stderr)
        return EXIT_EVIDENCE
    except (IngestionError, ValueError, KeyError, OSError) as error:
        print(json.dumps({"status": "rejected", "reason": str(error)}), file=sys.stderr)
        return EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())
