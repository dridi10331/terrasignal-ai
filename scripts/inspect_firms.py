from pathlib import Path

from terrasignal.data.firms import load_firms_csv


files = list(Path("data/raw").glob("*.csv"))

if not files:
    raise SystemExit("No FIRMS CSV found in data/raw/.")

df = load_firms_csv(files[0])

print(f"File: {files[0]}")
print(f"Valid rows: {len(df):,}")
print(f"Date range: {df['acq_date'].min()} to "
      f"{df['acq_date'].max()}")
print(f"Unique dates: {df['acq_date'].nunique():,}")

print("\nNumeric summary:")
print(df[["latitude", "longitude", "frp"]].describe())

print("\nMissing values:")
print(df.isna().sum())