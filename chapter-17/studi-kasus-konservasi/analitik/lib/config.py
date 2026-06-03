from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = CASE_ROOT / "data"
SUMBER = DATA_DIR / "sumber"
BRONZE = DATA_DIR / "bronze"
SILVER = DATA_DIR / "silver"
GOLD = DATA_DIR / "gold"
OUTPUT_DIR = CASE_ROOT / "output"

KAFKA_TOPIC_GPS = "gps.collar.leuser"
KAFKA_TOPIC_ALERT = "output.alert.konflik"

# Persamaan 17.2 — bobot indeks tekanan
BOBOT_TEKANAN = {"D": 0.30, "P": 0.25, "A": 0.20, "K": 0.15, "R": 0.10}

NDVI_DROP_THRESHOLD = 0.2
ALERT_JARAK_M = 2000
CRS_METRIC = "EPSG:32647"  # UTM 47N — Leuser

GAJAH = [
    ("G001", "Betina Dewasa Intan"),
    ("G002", "Jantan Dewasa Raja"),
    ("G003", "Betina Muda Sari"),
    ("G004", "Jantan Muda Bento"),
    ("G005", "Betina Dewasa Melati"),
    ("G006", "Jantan Dewasa Guntur"),
    ("G007", "Betina Muda Citra"),
]
