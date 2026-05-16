import pandas as pd
from typing import Any

def clean(raw: list[dict]) -> list[dict]:
    """Normalize a list of API records: drop nulls, strip strings, deduplicate."""
    if not raw:
        return []
    df = pd.DataFrame(raw)
    df = df.dropna(how="all")
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
    df = df.drop_duplicates()
    return df.to_dict(orient="records")

def flatten(nested: dict, prefix: str = "", sep: str = ".") -> dict:
    """Recursively flatten a nested dict for easy DB insertion."""
    items: dict[str, Any] = {}
    for key, val in nested.items():
        new_key = f"{prefix}{sep}{key}" if prefix else key
        if isinstance(val, dict):
            items.update(flatten(val, new_key, sep))
        else:
            items[new_key] = val
    return items

def normalize_api_response(payload: Any) -> list[dict]:
    """Accept a raw API payload (list or dict with data key) and return clean records."""
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = payload.get("data") or payload.get("results") or payload.get("items") or [payload]
    else:
        return []
    flattened = [flatten(r) if isinstance(r, dict) else {"value": r} for r in records]
    return clean(flattened)
