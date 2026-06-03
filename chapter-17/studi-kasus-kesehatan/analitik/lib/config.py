"""Konstanta lab — Stunting Sumatera Utara."""
from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = CASE_ROOT / "data"
SUMBER = DATA_DIR / "sumber"
BRONZE = DATA_DIR / "bronze"
SILVER = DATA_DIR / "silver"
GOLD = DATA_DIR / "gold"
OUTPUT_DIR = CASE_ROOT / "output"

TARGET_PREV_NASIONAL = 14.0  # % 2024
MIN_BALITA_DESA = 10
TOP_N_PER_KAB = 50

BOBOT_INDEKS = {
    "d1_prevalensi": 0.30,
    "d2_sanitasi": 0.20,
    "d3_kemiskinan": 0.20,
    "d4_akses": 0.20,
    "d5_air_bersih": 0.10,
}

KAFKA_TOPIC_UPLOAD = "balita.upload.sumut"
KAFKA_TOPIC_ALERT = "output.alert.kader"

# Simulasi kecepatan jalan (lab menggantikan OSRM)
KECEPATAN_RATA_KMH = 40.0
