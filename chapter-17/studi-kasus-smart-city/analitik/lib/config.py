from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = CASE_ROOT / "data"
SUMBER = DATA_DIR / "sumber"
BRONZE = DATA_DIR / "bronze"
SILVER = DATA_DIR / "silver"
GOLD = DATA_DIR / "gold"
OUTPUT_DIR = CASE_ROOT / "output"

KAFKA_BOOTSTRAP = "localhost:9097"
KAFKA_TOPIC_PROBE = "probe.kendaraan"
KAFKA_TOPIC_GPS_TMD = "gps.tmd"
KAFKA_TOPIC_SENSOR = "sensor.udara"
KAFKA_TOPIC_CCTV = "cctv.detektor"
KAFKA_TOPIC_KONDISI = "output.kondisi.jalan"

CRS_METRIC = "EPSG:32647"
MAP_MATCH_M = 50
MIN_PROBE_PER_RUAS = 3

# Ambang kemacetan (km/jam)
AMBANG_LANCAR = 40
AMBANG_PADAT = 20

TMD_RADIUS_M = 400
TMD_COVERAGE_MIN = 0.30

GRID_PM25_M = 500

# Faktor emisi lab (g/km) — disederhanakan IPCC Tier 1
EMISI_FAKTOR = {
    "mobil": {"co2": 120.0, "nox": 0.08, "pm25": 0.004},
    "motor": {"co2": 55.0, "nox": 0.02, "pm25": 0.002},
    "bus": {"co2": 650.0, "nox": 3.5, "pm25": 0.05},
    "angkot": {"co2": 280.0, "nox": 1.2, "pm25": 0.02},
}

ISPU_PM25 = [
    (0, 15.5, "BAIK", "#00e400"),
    (15.5, 55.4, "SEDANG", "#ffff00"),
    (55.5, 150.4, "TIDAK SEHAT", "#ff7e00"),
    (150.5, 250.4, "SANGAT TIDAK SEHAT", "#ff0000"),
    (250.5, 9999, "BERBAHAYA", "#7e0023"),
]

MEDAN_CENTER = (3.595, 98.672)
