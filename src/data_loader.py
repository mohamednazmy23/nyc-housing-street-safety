"""Load the processed tables in data/processed/ with the right column types.

The notebook writes the six tables in section 9.4. The website and any later notebook cell read them with
load_tables(), so everyone gets the same types (ZIP as text, counts as whole numbers, dates as dates).
Column meanings: docs/data_dictionary.md.
"""
from pathlib import Path

import pandas as pd

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
TABLE_NAMES = ["buildings", "crashes", "zip_year", "zip_month", "borough_year", "building_crash_counts"]
SIZE_GROUPS = ["Small (<50)", "Medium (50-199)", "Large (200+)"]

# Columns CSV can't type on its own: ZIP must stay text ("10451", not 10451), and whole-number columns
# with missing values need pandas' nullable "Int64"
TYPES = {
    "buildings": {"zip": "string", "street": "string", "building_id": "Int64", "project_id": "Int64",
                  "all_counted_units": "Int64", "total_units": "Int64", "completion_year": "Int64"},
    "crashes": {"zip": "string", "street": "string", "crash_id": "Int64", "hour": "Int64", "severe_injuries": "Int64",
                "fatalities": "Int64", "serious_harm": "Int64", "lookback_severe": "Int64",
                "repeat_location": "boolean"},
    "zip_year": {"zip": "string"},
    "zip_month": {"zip": "string"},
    "borough_year": {},
    "building_crash_counts": {"building_id": "Int64"},
}
DATES = {
    "buildings": ["project_start", "completion_date"],
    "crashes": ["crash_datetime", "month"],
    "zip_month": ["month"],
}


def load_table(name, folder=PROCESSED_DIR):
    """Read one processed table with its column types."""
    path = Path(folder) / f"{name}.csv"
    columns = pd.read_csv(path, nrows=0).columns
    types = dict(TYPES[name])
    if name == "buildings":   # all unit-breakdown columns are whole numbers
        types.update({col: "Int64" for col in columns if col.startswith("units_")})
    table = pd.read_csv(path, dtype=types, parse_dates=DATES.get(name, []))
    if "size_group" in table:
        table["size_group"] = pd.Categorical(table["size_group"], categories=SIZE_GROUPS, ordered=True)
    return table


def load_tables(folder=PROCESSED_DIR):
    """Read all six processed tables into a dict, e.g. data["zip_year"] (the `data` the charts receive)."""
    return {name: load_table(name, folder) for name in TABLE_NAMES}
