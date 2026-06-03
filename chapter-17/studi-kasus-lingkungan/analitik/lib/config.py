from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = CASE_ROOT / "data"
SUMBER = DATA_DIR / "sumber"
BRONZE = DATA_DIR / "bronze"
SILVER = DATA_DIR / "silver"
GOLD = DATA_DIR / "gold"
OUTPUT_DIR = CASE_ROOT / "output"

H3_RES = 7
KAFKA_TOPIC_FIRMS = "hotspot.firms.riau"
KAFKA_TOPIC_ISPA = "ispa.kecamatan.riau"

# Persamaan 17.1 — bobot komponen indeks risiko
BOBOT = {"G": 0.25, "F": 0.25, "H": 0.20, "N": 0.15, "D": 0.15}

# Faktor emisi lab (ton CO2e per ha gambut — Tier 1 disederhanakan)
EF_GAMBUT_TON_CO2E_PER_HA = 355.0
FRP_TO_HA = 0.3  # 1 MW FRP ≈ 0,3 ha (contoh buku)

KELAS_RISIKO = [
    (0.0, 0.2, "Sangat Rendah", "#9e9e9e"),
    (0.2, 0.4, "Rendah", "#4caf50"),
    (0.4, 0.6, "Sedang", "#ffeb3b"),
    (0.6, 0.8, "Tinggi", "#ff9800"),
    (0.8, 1.01, "Sangat Tinggi", "#f44336"),
]
