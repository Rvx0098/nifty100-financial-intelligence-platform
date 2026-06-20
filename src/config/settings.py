from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"
DATABASE = PROJECT_ROOT / "database" / "n100.db"