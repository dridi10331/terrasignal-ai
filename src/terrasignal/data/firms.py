from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "latitude",
    "longitude",
    "acq_date",
    "confidence",
    "frp",
}


def load_firms_csv(path: str | Path) -> pd.DataFrame:
    """Load a FIRMS CSV and perform basic data validation."""

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower()

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required FIRMS columns: {sorted(missing)}"
        )

    df["latitude"] = pd.to_numeric(
        df["latitude"], errors="coerce"
    )
    df["longitude"] = pd.to_numeric(
        df["longitude"], errors="coerce"
    )
    df["frp"] = pd.to_numeric(df["frp"], errors="coerce")
    df["acq_date"] = pd.to_datetime(
        df["acq_date"], errors="coerce"
    )

    df = df.dropna(
        subset=["latitude", "longitude", "acq_date"]
    ).copy()

    valid_coordinates = (
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    )

    df = df.loc[valid_coordinates].copy()

    df["acq_date"] = df["acq_date"].dt.floor("D")

    return df.reset_index(drop=True)