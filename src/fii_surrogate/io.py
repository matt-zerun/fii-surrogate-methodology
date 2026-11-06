from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        return pd.read_excel(path)
    if path.suffix.lower() == ".csv":
        try:
            return pd.read_csv(path)
        except UnicodeDecodeError:
            return pd.read_csv(path, sep=";", encoding="cp1250")
    raise ValueError(f"Unsupported input format: {path.suffix}. Use CSV or XLSX.")
