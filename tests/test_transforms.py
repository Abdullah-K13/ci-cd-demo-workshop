import pandas as pd
import pytest

from transforms import add_total, drop_bad_rows, revenue_by_city, validate_columns


def frame(rows):
    return pd.DataFrame(
        rows, columns=["order_id", "date", "city", "item", "qty", "price"]
    )


def test_validate_columns_accepts_a_good_frame():
    df = frame([[1, "2026-10-18", "Karachi", "Leash", 2, 500]])
    assert validate_columns(df) is df


def test_validate_columns_rejects_a_missing_column():
    df = pd.DataFrame({"order_id": [1]})
    with pytest.raises(ValueError, match="missing columns"):
        validate_columns(df)


def test_drop_bad_rows_removes_zero_quantity():
    df = frame([
        [1, "2026-10-18", "Karachi", "Leash", 2, 500],
        [2, "2026-10-18", "Lahore", "Leash", 0, 500],
    ])
    assert len(drop_bad_rows(df)) == 1


def test_drop_bad_rows_removes_a_bad_date():
    df = frame([
        [1, "2026-10-18", "Karachi", "Leash", 2, 500],
        [2, "not-a-date", "Lahore", "Leash", 1, 500],
    ])
    assert len(drop_bad_rows(df)) == 1


def test_add_total_multiplies_qty_by_price():
    df = add_total(frame([[1, "2026-10-18", "Karachi", "Leash", 3, 500]]))
    assert df.loc[0, "total"] == 1500


def test_revenue_by_city_sorts_biggest_first():
    df = add_total(frame([
        [1, "2026-10-18", "Karachi", "Leash", 1, 100],
        [2, "2026-10-18", "Lahore", "Leash", 5, 100],
    ]))
    out = revenue_by_city(df)
    assert list(out["city"]) == ["Lahore", "Karachi"]
