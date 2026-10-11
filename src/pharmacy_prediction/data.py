
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "pharma-data.csv"

REQUIRED_COLUMNS = [
    "Customer Name", "Channel", "Country",
    "Month", "Year", "Sales", "Quantity"
]


def load_data_raw():
    """Load the raw pharmaceutical sales dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    return df


def validate_columns(df):
    """Check that the required columns exist."""

    missing_columns = [
        col for col in REQUIRED_COLUMNS if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def prepare_data(df):
    """Basic data preparation."""

    df = df.copy()

    text_columns = ["Customer Name", "Channel", "Country", "Month"]

    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    df["order_month"] = pd.to_datetime(
        df["Month"] + " " + df["Year"].astype(str),
        format="%B %Y",
        errors="coerce"
    )

    if df["order_month"].isna().any():
        raise ValueError("Invalid dates found in the dataset")

    return df


def filter_pharmacies(df):
    """Keep pharmacy accounts in Germany."""

    df = df[
        (df["Channel"] == "Pharmacy") &
        (df["Country"] == "Germany")
    ].copy()

    return df


if __name__ == "__main__":

    df = load_data_raw()

    validate_columns(df)

    df = prepare_data(df)
    df = filter_pharmacies(df)

    print("Shape:", df.shape)
    print("Unique pharmacies:", df["Customer Name"].nunique())
    print("Date range:", df["order_month"].min(), "to", df["order_month"].max())
    print("Non-positive sales:", (df["Sales"] <= 0).sum())

    print("\nFirst 5 rows:")
    print(df.head())
