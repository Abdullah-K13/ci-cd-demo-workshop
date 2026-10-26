"""Entry point. Reads a CSV, runs the transforms, prints a summary."""
import os
import sys

import pandas as pd

from transforms import add_total, drop_bad_rows, revenue_by_city, validate_columns

DATA_DIR = os.getenv("DATA_DIR", "data")


def main(path=None):
    path = path or os.path.join(DATA_DIR, "sales.csv")
    if not os.path.exists(path):
        print(f"ERROR: no input file at {path}", file=sys.stderr)
        return 2

    df = pd.read_csv(path)
    df = validate_columns(df)
    df = add_total(drop_bad_rows(df))

    print(f"{len(df)} clean rows")
    print(revenue_by_city(df).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else None))
