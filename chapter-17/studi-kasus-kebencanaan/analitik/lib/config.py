"""Path dan konstanta lab — DAS Musi."""
from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = CASE_ROOT / "data"
SUMBER = DATA_DIR / "sumber"
BRONZE = DATA_DIR / "bronze"
SILVER = DATA_DIR / "silver"
GOLD = DATA_DIR / "gold"
OUTPUT_DIR = CASE_ROOT / "output"

# Ambang TMA stasiun referensi Kayu Agung (cm) — sesuai panduan arsitektur
TMA_HIJAU_MAX = 650
TMA_KUNING_MAX = 850
TMA_ORANYE_MAX = 1020

# Curah hujan kumulatif 3 jam (mm)
HUJAN_KUNING_MIN = 30
HUJAN_ORANYE_MIN = 50
HUJAN_MERAH_MIN = 80

CRS_WGS84 = "EPSG:4326"
CRS_METRIC = "EPSG:32748"  # UTM 48S — Sumatera Selatan

KAFKA_TOPIC_TMA = "sensor.tma.musi"
STASIUN_REF = "KAYU_AGUNG"
