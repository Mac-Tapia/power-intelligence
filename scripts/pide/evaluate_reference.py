"""Offline CLI: run an illustrative study audit (never an official compliance report)."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages/python/power-regulation/src"))
from unitesis_regulation.pide_reference import ReferenceGateError, assess_reference_case


def main():
    p = argparse.ArgumentParser(
        description="Audit historical TDR-based PIDE study; NOT official approval"
    )
    p.add_argument("--input", required=True, type=Path)
    a = p.parse_args()
    try:
        payload = json.loads(a.input.read_text(encoding="utf-8"))
        answer = assess_reference_case(payload)
    except (OSError, ValueError, ReferenceGateError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(answer, ensure_ascii=False, indent=2))
    return 0 if answer["documentary_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
