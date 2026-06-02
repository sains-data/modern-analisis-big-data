"""Path kerja lab Chapter 7 (relatif ke Konfigurasi-lab/)."""
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = LAB_ROOT / "data"
DATALAKE = LAB_ROOT / "datalake"

BRONZE_TRX = DATALAKE / "bronze" / "transaksi"
SILVER_TRX = DATALAKE / "silver" / "transaksi"
GOLD_DIR = DATALAKE / "gold"

DATA_TRX_CSV = DATA_DIR / "transaksi.csv"
DATA_PLG_CSV = DATA_DIR / "pelanggan.csv"
BRONZE_BATCH = BRONZE_TRX / "batch_001.parquet"
