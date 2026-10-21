"""Build a supervised forecasting dataset from a CSV time series.

  python scripts/datasets/build_dataset.py --input fixtures/timeseries/synthetic_feeder_load.csv \
      --output local-data/datasets/synthetic --timestamp timestamp --target p_mw --freq 15min
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for source in sorted((ROOT / "packages/python").glob("*/src")):
    sys.path.insert(0, str(source))

from unitesis_application.datasets import build_forecast_dataset  # noqa: E402
from unitesis_sciml.datasets import DatasetError, DatasetSpec  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--timestamp", default="timestamp")
    p.add_argument("--target", required=True)
    p.add_argument("--freq", required=True, help="pandas frequency, e.g. 15min or h")
    p.add_argument("--horizon", type=int, default=1)
    p.add_argument("--lags", default="1,2,3,4,96,672")
    p.add_argument("--seasonal-lag", type=int, default=672)
    a = p.parse_args()
    spec = DatasetSpec(a.timestamp, a.target, a.freq, horizon_steps=a.horizon,
                       lags=tuple(int(x) for x in a.lags.split(",")),
                       seasonal_lag=a.seasonal_lag)
    try:
        manifest = build_forecast_dataset(a.input, a.output, spec)
    except (DatasetError, OSError) as error:
        print(json.dumps({"status": "rejected", "reason": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps({"dataset_sha256": manifest["dataset_sha256"],
                      "quality": manifest["quality"],
                      "splits": {k: v["rows"] for k, v in manifest["splits"].items()},
                      "output": str(a.output.resolve())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
