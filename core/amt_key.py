"""AMT key — a trailing NEO/LAO column joining AssetName + ComponentCode + ModifierCode
into one compound key for downstream AMT/Snowflake population to join on, instead of
matching three separate columns by hand.

Not customer-specific: AssetName/ComponentCode/ModifierCode are already treated as "the
AMT-key pair/fields" everywhere else in this project (see core/cross_reference.py's
module docstring and core/exceptions.py's split_blank_pair) — this just makes that
existing concept a real, visible column instead of an implicit convention, for every
customer's NEO/LAO alike. The format (straight concatenation, no separator) matches
BHP's own working file (test-data/New-BHP-Workfile/BHP Workfile Sep26.xlsx), whose NEO
tab already builds an identical "Key1" column (`=AD2&I2&J2` — Asset & ComponentCode &
ModifierCode) by hand for this exact purpose.
"""
from __future__ import annotations
import pandas as pd

_KEY_FIELDS = ("AssetName", "ComponentCode", "ModifierCode")


def compute(out: pd.DataFrame) -> pd.Series:
    """AssetName + ComponentCode + ModifierCode, blank-safe (missing/NaN -> ""), for
    every row in `out`. A row missing one of the three still gets a (partial, honestly
    incomplete) key rather than being dropped or blanked entirely — same "print exactly
    what's known, invent nothing" rule as every other column in this project.
    """
    if out.empty:
        return pd.Series([], index=out.index, dtype="object")

    parts = [
        out[col].fillna("").astype(str) if col in out.columns
        else pd.Series([""] * len(out), index=out.index)
        for col in _KEY_FIELDS
    ]
    return parts[0] + parts[1] + parts[2]
