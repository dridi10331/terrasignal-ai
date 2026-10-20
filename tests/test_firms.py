import pandas as pd
import pytest

from terrasignal.data.firms import load_firms_csv


def test_loader_normalizes_columns_and_dates(tmp_path):
    path = tmp_path / "sample.csv"

    pd.DataFrame({
        " latitude ": [36.8, 91.0],
        "longitude": [10.2, 10.0],
        "acq_date": ["2023-07-01", "2023-07-01"],
        "confidence": ["high", "low"],
        "frp": [12.5, 8.0],
    }).to_csv(path, index=False)

    df = load_firms_csv(path)

    assert len(df) == 1
    assert df.iloc[0]["latitude"] == 36.8
    assert pd.api.types.is_datetime64_any_dtype(
        df["acq_date"]
    )


def test_loader_rejects_missing_columns(tmp_path):
    path = tmp_path / "invalid.csv"

    pd.DataFrame({
        "latitude": [36.8],
    }).to_csv(path, index=False)

    with pytest.raises(
        ValueError,
        match="Missing required FIRMS columns",
    ):
        load_firms_csv(path)