from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

def save_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def save_csv(rows: list[dict], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)

def maybe_save_excel(rows: list[dict], path: Path):
    try:
        pd.DataFrame(rows).to_excel(path, index=False)
    except Exception:
        pass
