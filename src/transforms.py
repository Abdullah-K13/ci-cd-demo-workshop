"""Pure functions for the sales pipeline.

Pure means: same input, same output, no database, no files. That is exactly
what makes them easy to test, which is exactly what makes CI useful.
hello this is abdulla testing
"""
import pandas as pd

REQUIRED_COLUMNS = ["order_id", "date", "city", "item", "qty", "price"]



def validate_columns(df):
    """Raise if the incoming file is not the shape we expect."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    return df


def drop_bad_rows(df):
    """Remove rows we cannot use: no quantity, no city, unparseable date."""
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["order_id", "date", "city"])
    df = df[df["qty"] > 0]
    return df.reset_index(drop=True)


def add_total(df):
    """Line total = quantity x unit price."""
    df = df.copy()
    df["total"] = df["qty"] * df["price"]
    return df


def revenue_by_city(df):
    """Total revenue per city, biggest first."""
    return (
        df.groupby("city")["total"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
