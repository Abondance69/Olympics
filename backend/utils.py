import os
import json
import joblib
import pandas as pd
from typing import Any, Dict, Optional

def safe_load_json(path: str) -> Optional[Dict[str, Any]]:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_load_model(path: str):
    if not os.path.exists(path):
        return None
    return joblib.load(path)

def ensure_columns(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for c in cols:
        if c not in df.columns:
            df[c] = None
    return df
