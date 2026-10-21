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


DEFAULT_CRITERIA = {"v_min_pu": 0.95, "max_loading_percent": 100.0}


def resolve_criteria(a: argparse.Namespace) -> dict[str, Any]:
    """Explicit flag > application case (planning_criteria) > labelled non-regulatory default."""
    case_criteria: dict[str, Any] = {}
    source = "default_not_regulatory"
    if getattr(a, "case", None):
        from unitesis_config import load_case

        case_criteria = load_case(ROOT / "config/cases" / f"{a.case}.json").planning_criteria
        if case_criteria:
            source = f"case:{a.case} ({case_criteria.get('source', '')[:80]})"
    out: dict[str, Any] = {}
    for key in ("v_min_pu", "max_loading_percent"):
        flag = getattr(a, key)
        out[key] = flag if flag is not None else case_criteria.get(key, DEFAULT_CRITERIA[key])
    explicit = [k for k in ("v_min_pu", "max_loading_percent") if getattr(a, k) is not None]
    out["source"] = source + (f"; explicit override: {explicit}" if explicit else "")
    return out


def _print(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_study(a: argparse.Namespace) -> int:
    from unitesis_application.study import engine_by_name, run_study

    if a.engine == "3ph":
        from unitesis_application.unbalanced_study import run_unbalanced_study

        result = run_unbalanced_study(a.input, a.output, scenario_id=a.scenario)
        cand = result["candidate"]
        _print({"status": result["status"], "snapshot_sha256": result["snapshot_sha256"],
                "iterations": cand["iterations"], "residual_mva": cand["residual_mva"],
                "comparison": result["comparison"]["status"],
                "messages": cand["messages"],
                "evidence": str(Path(a.output).resolve()), "technical_acceptance": False})
        return EXIT_UNAVAILABLE if result["status"] == "computed" else EXIT_NOT_CONVERGED

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

    crit = resolve_criteria(a)
    result = run_new_load_study(a.input, a.output, load_id=a.load_id, bus=a.bus, p_mw=a.p_mw,
                                q_mvar=a.q_mvar, v_min_pu=crit["v_min_pu"],
                                max_loading_percent=crit["max_loading_percent"],
                                criteria_source=crit["source"],
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
        operating_temperature_c=a.temperature_c, phase_gmd_m=a.gmd_m,
        v_min_pu=resolve_criteria(a)["v_min_pu"],
        max_loading_percent=resolve_criteria(a)["max_loading_percent"])
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


def cmd_profile_export(a: argparse.Namespace) -> int:
    from unitesis_adapters.format_profile import profile_export, structure_only
    from unitesis_evidence.store import publish_evidence

    profile = profile_export({"network": a.network, "loads": a.loads,
                              "equipment": a.equipment})
    publish_evidence(a.output, profile)
    if a.structure_output:
        a.structure_output.write_text(json.dumps(structure_only(profile), indent=1,
                                                 ensure_ascii=False) + "\n", encoding="utf-8")
    _print({"unread_sections_with_rows": profile["unread_sections_with_rows"],
            "evidence": str(Path(a.output).resolve())})
    return EXIT_OK


def cmd_distill_pf(a: argparse.Namespace) -> int:
    from unitesis_application.distillation_study import run_pf_distillation

    result = run_pf_distillation(a.dataset_dir, a.output, a.models_dir, select=a.select,
                                 epochs=a.epochs, seed=a.seed,
                                 student_hidden=a.student_hidden,
                                 student_layers=a.student_layers)
    models = result["report"]["models"]
    _print({name: {"parameters": m["parameters"],
                   "test_p95_pu": m["test"].get("p95_abs_error_pu"),
                   "test_gate": m["test"].get("gate_ac_006_02"),
                   "latency_ms": round(m["latency_ms_per_scenario"], 4)}
            for name, m in models.items()}
           | {"distillation_effect_test_p95_pu":
                  result["report"]["distillation_effect_test_p95_pu"],
              "evidence": str(Path(a.output).resolve()), "technical_acceptance": False})
    return EXIT_OK


def cmd_eval_pf_baseline(a: argparse.Namespace) -> int:
    from unitesis_application.pf_baselines import evaluate_baseline

    r = evaluate_baseline(a.networks_dir, a.dataset_dir, a.output, split=a.split,
                          v_min_pu=a.v_min_pu)
    _print({"surrogate": r["surrogate"], "split": r["split"], "feeders": r["feeders"],
            "overall": r["overall"], "evidence": str(Path(a.output).resolve())})
    return EXIT_OK


def cmd_hosting_capacity(a: argparse.Namespace) -> int:
    from unitesis_adapters.neutral_json import ingest_file
    from unitesis_application.hosting_capacity import run_hosting_capacity
    from unitesis_topology import build_energized_network

    ingestion = ingest_file(a.input)
    snapshot = ingestion.require_snapshot()
    buses = (list(build_energized_network(snapshot).nodes)[1:] if a.buses == "all"
             else a.buses.split(","))
    steps = [round(a.p_step_mw * k, 6) for k in range(1, int(a.p_max_mw / a.p_step_mw) + 1)]
    crit = resolve_criteria(a)
    r = run_hosting_capacity(snapshot, a.output, buses=buses, p_levels_mw=steps,
                             power_factor=a.pf, v_min_pu=crit["v_min_pu"],
                             max_loading_percent=crit["max_loading_percent"],
                             margin_pu=a.margin_pu, source_manifest=ingestion.manifest,
                             criteria_source=crit["source"])
    limits = [b["confirmed_limit_mw"] for b in r["buses"] if "confirmed_limit_mw" in b]
    _print({"base_case": r["base_case"], "buses": len(r["buses"]),
            "solver_calls": r["solver_calls"],
            "agreement_rate": r["agreement_rate"],
            "min_limit_mw": min(limits, default=None), "max_limit_mw": max(limits, default=None),
            "evidence": str(Path(a.output).resolve()), "technical_acceptance": False})
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
    uvicorn.run(app, host=a.host, port=a.port, access_log=False)
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="unitesis", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    def postgres_worker(a):
        from unitesis_adapters.postgres_repository import PostgresJobRepository, PostgresRepository
        from unitesis_application.job_execution import execute_persisted_job

        dsn = os.environ.get(a.dsn_env)
        if not dsn:
            raise ValueError("PostgreSQL DSN environment variable is missing")
        repo = PostgresRepository(dsn, namespace=a.namespace, initialize=a.initialize)
        jobs = PostgresJobRepository(dsn, namespace=a.namespace)
        if a.initialize:
            _print({"schema_initialized": True, "namespace": a.namespace})
            return EXIT_OK
        if not a.job_id:
            raise ValueError("job-id is required to execute a persisted request")
        result = execute_persisted_job(repo, jobs, a.job_id,
                                      catalogs=ROOT / "config/catalogs/conductors")
        _print({"job_id": result["job_id"], "status": result["status"],
                "comparison": result.get("comparison")})
        return EXIT_OK if result["status"] == "finished" else EXIT_NOT_CONVERGED

    s = sub.add_parser("postgres-worker", help="initialize sandbox schema or execute a durable job")
    s.add_argument("--dsn-env", default="UNITESIS_POSTGRES_DSN")
    s.add_argument("--namespace", default="unitesis")
    s.add_argument("--initialize", action="store_true")
    s.add_argument("--job-id")
    s.set_defaults(func=postgres_worker)

    def promote(a):
        from unitesis_application.pf_dataset import promote_pf_dataset
        from unitesis_config import load_case

        case = load_case(ROOT / "config/cases" / f"{a.case}.json")
        registry = json.loads((ROOT / "config/datasets/sources.v2.json").read_text(
            encoding="utf-8"))
        _print(promote_pf_dataset(case, a.dataset_dir, a.output, source_registry=registry))
        return EXIT_OK

    s = sub.add_parser("promote-pf-dataset", help="verify candidate bytes/splits and attest gold")
    s.add_argument("--case", required=True)
    s.add_argument("--dataset-dir", type=Path, required=True)
    s.add_argument("--output", type=Path, required=True)
    s.set_defaults(func=promote)

    def io(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--input", type=Path, required=True)
        sp.add_argument("--output", type=Path, required=True)

    def engine(sp: argparse.ArgumentParser, three_phase: bool = False) -> None:
        sp.add_argument("--engine", choices=("nr", "bfs", "3ph") if three_phase else ("nr", "bfs"),
                        default="nr",
                        help="own engine: nr = Newton-Raphson (radial/meshed), bfs = radial "
                             "sweep" + (", 3ph = three-phase unbalanced (008-C)"
                                        if three_phase else ""))

    def criteria(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--case", help="take planning criteria from this application case")
        sp.add_argument("--v-min-pu", type=float, default=None)
        sp.add_argument("--max-loading-percent", type=float, default=None)

    s = sub.add_parser("study", help="power flow + independent comparison + evidence")
    io(s)
    s.add_argument("--scenario", default="base")
    engine(s, three_phase=True)
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

    s = sub.add_parser("build-pf-dataset", help="labelled power-flow scenarios (spec 029)")
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

    s = sub.add_parser("eval-pf-baseline", help="score the physics baseline (AC-029-S06)")
    s.add_argument("--networks-dir", type=Path, required=True)
    s.add_argument("--dataset-dir", type=Path, required=True)
    s.add_argument("--output", type=Path, required=True)
    s.add_argument("--split", choices=("train", "valid", "test"), default="test")
    s.add_argument("--v-min-pu", type=float, default=0.95)
    s.set_defaults(func=cmd_eval_pf_baseline)

    s = sub.add_parser("profile-export",
                       help="reverse-engineer an export's structure vs reader coverage (REA)")
    s.add_argument("--network", type=Path, required=True)
    s.add_argument("--loads", type=Path, required=True)
    s.add_argument("--equipment", type=Path, required=True)
    s.add_argument("--output", type=Path, required=True, help="full profile (local evidence)")
    s.add_argument("--structure-output", type=Path,
                   help="redacted structure without values, safe to version")
    s.set_defaults(func=cmd_profile_export)

    s = sub.add_parser("distill-pf-surrogate",
                       help="teacher -> student distillation of the PF surrogate (029, ADR-0011)")
    s.add_argument("--dataset-dir", type=Path, required=True)
    s.add_argument("--output", type=Path, required=True)
    s.add_argument("--models-dir", type=Path, required=True, help="outside Git (local-data)")
    s.add_argument("--epochs", type=int, default=60)
    s.add_argument("--seed", type=int, default=7)
    s.add_argument("--student-hidden", type=int, default=32)
    s.add_argument("--student-layers", type=int, default=3)
    s.add_argument("--select", action="store_true",
                   help="choose the architecture on the validation split (declared grid)")
    s.set_defaults(func=cmd_distill_pf)

    s = sub.add_parser("hosting-capacity", help="remaining capacity per bus (002/006)")
    io(s)
    s.add_argument("--buses", default="all", help="'all' or comma-separated bus ids")
    s.add_argument("--p-max-mw", type=float, required=True)
    s.add_argument("--p-step-mw", type=float, required=True)
    s.add_argument("--pf", type=float, required=True, help="power factor of the new load")
    s.add_argument("--margin-pu", type=float, default=0.005,
                   help="voltage margin applied to the surrogate screening")
    criteria(s)
    s.set_defaults(func=cmd_hosting_capacity)

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
