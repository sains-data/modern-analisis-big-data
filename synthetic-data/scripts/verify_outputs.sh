#!/usr/bin/env bash
# Verifikasi volume & integritas output generator.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${ROOT}/outputs"
FAIL=0

check_lines() {
  local file="$1" expected="$2" label="$3"
  if [[ ! -f "${file}" ]]; then
    echo "[FAIL] ${label}: file tidak ada — ${file}"
    FAIL=1
    return
  fi
  local count
  count="$(wc -l < "${file}" | tr -d ' ')"
  if [[ "${count}" -ne "${expected}" ]]; then
    echo "[FAIL] ${label}: ${count} baris (harapan ${expected}) — ${file}"
    FAIL=1
  else
    echo "[OK]   ${label}: ${count} baris"
  fi
}

check_json_array() {
  local file="$1" expected="$2" label="$3"
  if [[ ! -f "${file}" ]]; then
    echo "[FAIL] ${label}: file tidak ada — ${file}"
    FAIL=1
    return
  fi
  local count
  count="$(.venv/bin/python -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "${file}")"
  if [[ "${count}" -ne "${expected}" ]]; then
    echo "[FAIL] ${label}: ${count} record (harapan ${expected}) — ${file}"
    FAIL=1
  else
    echo "[OK]   ${label}: ${count} record"
  fi
}

echo "=== Verifikasi output sintesis ==="
echo "Direktori: ${OUT}"
echo ""

if [[ ! -d "${OUT}" ]]; then
  echo "[FAIL] Folder outputs/ belum ada. Jalankan: bash scripts/generate.sh"
  exit 1
fi

# CSV (termasuk header)
check_lines "${OUT}/ch03_minio/sample_users.csv"           52  "ch03 sample_users (50 + 1 duplikat + header)"
check_lines "${OUT}/ch04_hadoop/latihan.txt"                  7  "ch04 latihan.txt (7 kalimat)"
check_lines "${OUT}/ch04_hadoop/dataset_wordcount.txt"        6  "ch04 dataset_wordcount (6 baris)"
check_lines "${OUT}/ch05_spark/mahasiswa.csv"              11  "ch05 mahasiswa (10 + header)"
check_lines "${OUT}/ch06_medallion/pelanggan.csv"           8  "ch06 pelanggan (7 + header)"
check_lines "${OUT}/ch06_medallion/transaksi.csv"          17  "ch06 transaksi (15 + anomali + header)"
check_lines "${OUT}/ch07_medallion_local/transaksi.csv"    17  "ch07 transaksi (salinan ch06)"
check_lines "${OUT}/ch08_storage/pelanggan.csv"            51  "ch08 pelanggan (50 + header)"
check_lines "${OUT}/ch08_storage/transaksi.csv"           501  "ch08 transaksi (500 + header)"
check_lines "${OUT}/ch09_orchestration/transaksi_harian.csv" 101 "ch09 transaksi harian (100 + header)"
check_lines "${OUT}/ch09_orchestration/catatan_aktivitas_harian.csv" 101 "ch09 catatan kanonik (100 + header)"
check_lines "${OUT}/ch11_ml/transaksi_ml.csv"           10001  "ch11 transaksi_ml (10000 + header)"
check_json_array "${OUT}/ch11_ml/pelanggan_agregat.json" 200 "ch11 pelanggan agregat"
check_lines "${OUT}/ch12_viz/silver_transaksi.csv"      15001  "ch12 silver (15000 + header)"
check_lines "${OUT}/ch14_e2e/silver_transaksi.csv"      15001  "ch14 silver (15000 + header)"
check_lines "${OUT}/ch14_e2e/gold_tren_bulanan.csv"        13  "ch14 gold tren_bulanan (12 + header)"
check_lines "${OUT}/ch14_e2e/gold_tren_lanjutan.csv"       13  "ch14 gold tren_lanjutan (12 + header)"
check_lines "${OUT}/ch14_e2e/gold_omzet_kelas.csv"          7  "ch14 gold omzet_kelas (6 + header)"
check_lines "${OUT}/ch14_e2e/gold_omzet_geografis.csv"     11  "ch14 gold omzet_geografis (10 + header)"
check_lines "${OUT}/ch14_e2e/gold_segmentasi_rfm.csv"     301  "ch14 gold segmentasi_rfm (300 + header)"
check_lines "${OUT}/ch12_viz/gold_tren_bulanan.csv"        13  "ch12 gold tren_bulanan (12 + header)"
check_lines "${OUT}/ch12_viz/gold_tren_lanjutan.csv"       13  "ch12 gold tren_lanjutan (12 + header)"
check_lines "${OUT}/ch12_viz/gold_omzet_kelas.csv"          7  "ch12 gold omzet_kelas (6 + header)"
check_lines "${OUT}/ch12_viz/gold_omzet_geografis.csv"     11  "ch12 gold omzet_geografis (10 + header)"
check_lines "${OUT}/ch12_viz/gold_segmentasi_rfm.csv"     301  "ch12 gold segmentasi_rfm (300 + header)"

# JSON
check_json_array "${OUT}/ch10_streaming/sample_events.json"          10 "ch10 sample_events"
check_json_array "${OUT}/ch10_streaming/transaksi_historis.json"    100 "ch10 transaksi_historis"
check_json_array "${OUT}/ch10_streaming/sensor_iot_historis.json"   100 "ch10 sensor_iot"
check_json_array "${OUT}/ch10_streaming/transaksi_duplikat_test.json" 50 "ch10 duplikat_test"
check_json_array "${OUT}/ch10_streaming/catatan_aktivitas_streaming.json" 100 "ch10 catatan kanonik"
check_json_array "${OUT}/ch10_streaming/pembacaan_sensor.json" 100 "ch10 sensor kanonik"

# Constraint spot-check via Python
echo ""
echo "=== Spot-check constraint ==="
.venv/bin/python - <<'PY' "${OUT}" || FAIL=1
import csv, json, sys
from pathlib import Path

out = Path(sys.argv[1])
errors = []

# ch03: null pendapatan baris ke-3
rows = list(csv.DictReader((out / "ch03_minio/sample_users.csv").open()))
if rows[2].get("salary") not in ("", None):
    errors.append("ch03: baris 3 salary harus null")

# ch06: duplikat TRX001
trx = list(csv.DictReader((out / "ch06_medallion/transaksi.csv").open()))
ids = [r["id_transaksi"] for r in trx]
if ids.count("TRX001") < 2:
    errors.append("ch06: duplikat TRX001 tidak ditemukan")

# ch11: nilai_total konsisten
for i, row in enumerate(csv.DictReader((out / "ch11_ml/transaksi_ml.csv").open())):
    q = float(row["kuantitas"])
    h = float(row["harga_satuan"])
    d = float(row["diskon"])
    t = float(row["total_nilai"])
    exp = round(q * h * (1 - d), 2)
    if abs(t - exp) > 0.02:
        errors.append(f"ch11 baris {i+1}: nilai_total {t} != {exp}")
        break

# ch10 streaming alias
ev = json.load((out / "ch10_streaming/sample_events.json").open())
if ev and "user_id" not in ev[0]:
    errors.append("ch10: field user_id tidak ada")

if errors:
    for e in errors:
        print(f"[FAIL] {e}")
    sys.exit(1)
print("[OK]   Constraint spot-check lulus")
PY

echo ""
if [[ "${FAIL}" -eq 0 ]]; then
  echo "=== SEMUA VERIFIKASI LULUS ==="
  exit 0
else
  echo "=== ADA VERIFIKASI GAGAL ==="
  exit 1
fi
