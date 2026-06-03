#!/usr/bin/env bash
# Salin output sintesis ke folder Konfigurasi-lab masing-masing bab.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="$(cd "${ROOT}/.." && pwd)"
OUT="${ROOT}/outputs"
DRY="${DRY_RUN:-0}"

copy() {
  local src="$1" dst="$2"
  if [[ ! -f "${src}" ]]; then
    echo "[SKIP] Sumber tidak ada: ${src}"
    return
  fi
  mkdir -p "$(dirname "${dst}")"
  if [[ "${DRY}" == "1" ]]; then
    echo "[dry-run] ${src} -> ${dst}"
  else
    cp "${src}" "${dst}"
    echo "[sync] ${dst}"
  fi
}

echo "=== Sync data sintesis ke chapter lab ==="
echo "Repo root: ${REPO}"
echo "Output:    ${OUT}"
echo ""

if [[ ! -d "${OUT}" ]]; then
  echo "Error: outputs/ belum ada. Jalankan: bash scripts/generate.sh"
  exit 1
fi

# Bab 3 — MinIO raw-data
copy "${OUT}/ch03_minio/sample_users.csv" \
     "${REPO}/chapter-3/Konfigurasi-lab/raw-data/sample_users.csv"

# Bab 4 — HDFS teks (latihan + WordCount)
copy "${OUT}/ch04_hadoop/latihan.txt" \
     "${REPO}/chapter-4/Konfigurasi-lab/data/latihan.txt"
copy "${OUT}/ch04_hadoop/dataset_wordcount.txt" \
     "${REPO}/chapter-4/Konfigurasi-lab/data/dataset_wordcount.txt"

# Bab 5 — Spark intro
copy "${OUT}/ch05_spark/mahasiswa.csv" \
     "${REPO}/chapter-5/Konfigurasi-lab/data/mahasiswa.csv"
copy "${OUT}/ch05_spark/skor_kompetensi.csv" \
     "${REPO}/chapter-5/Konfigurasi-lab/data/skor_kompetensi.csv"

# Bab 6 — Medallion HDFS
copy "${OUT}/ch06_medallion/transaksi.csv" \
     "${REPO}/chapter-6/Konfigurasi-lab/data/transaksi.csv"
copy "${OUT}/ch06_medallion/pelanggan.csv" \
     "${REPO}/chapter-6/Konfigurasi-lab/data/pelanggan.csv"
copy "${OUT}/ch06_medallion/entitas_partisipan.csv" \
     "${REPO}/chapter-6/Konfigurasi-lab/data/entitas_partisipan.csv"
copy "${OUT}/ch06_medallion/catatan_aktivitas.csv" \
     "${REPO}/chapter-6/Konfigurasi-lab/data/catatan_aktivitas.csv"

# Bab 7 — Medallion lokal (Arrow) — dataset identik Bab 6
copy "${OUT}/ch07_medallion_local/transaksi.csv" \
     "${REPO}/chapter-7/Konfigurasi-lab/data/transaksi.csv"
copy "${OUT}/ch07_medallion_local/pelanggan.csv" \
     "${REPO}/chapter-7/Konfigurasi-lab/data/pelanggan.csv"
copy "${OUT}/ch06_medallion/entitas_partisipan.csv" \
     "${REPO}/chapter-7/Konfigurasi-lab/data/entitas_partisipan.csv"
copy "${OUT}/ch06_medallion/catatan_aktivitas.csv" \
     "${REPO}/chapter-7/Konfigurasi-lab/data/catatan_aktivitas.csv"

# Bab 8 — Hive + HBase
copy "${OUT}/ch08_storage/transaksi.csv" \
     "${REPO}/chapter-8/Konfigurasi-lab/data/transaksi.csv"
copy "${OUT}/ch08_storage/pelanggan.csv" \
     "${REPO}/chapter-8/Konfigurasi-lab/data/pelanggan.csv"
copy "${OUT}/ch08_storage/entitas_partisipan.csv" \
     "${REPO}/chapter-8/Konfigurasi-lab/data/entitas_partisipan.csv"
copy "${OUT}/ch08_storage/catatan_aktivitas.csv" \
     "${REPO}/chapter-8/Konfigurasi-lab/data/catatan_aktivitas.csv"

# Bab 9 — Orkestrasi Airflow (referensi harian)
copy "${OUT}/ch09_orchestration/transaksi_harian.csv" \
     "${REPO}/chapter-9/Konfigurasi-lab/data/transaksi_harian.csv"
copy "${OUT}/ch09_orchestration/catatan_aktivitas_harian.csv" \
     "${REPO}/chapter-9/Konfigurasi-lab/data/catatan_aktivitas_harian.csv"

# Bab 10 — Streaming Kafka
for f in transaksi_historis.json sample_events.json sensor_iot_historis.json transaksi_duplikat_test.json; do
  copy "${OUT}/ch10_streaming/${f}" \
       "${REPO}/chapter-10/Konfigurasi-lab/data/${f}"
  copy "${OUT}/ch10_streaming/${f}" \
       "${REPO}/chapter-10/Data/${f}"
done
copy "${OUT}/ch10_streaming/catatan_aktivitas_streaming.json" \
     "${REPO}/chapter-10/Konfigurasi-lab/data/catatan_aktivitas_streaming.json"
copy "${OUT}/ch10_streaming/pembacaan_sensor.json" \
     "${REPO}/chapter-10/Konfigurasi-lab/data/pembacaan_sensor.json"

# Bab 11 — ML
copy "${OUT}/ch11_ml/transaksi_ml.csv" \
     "${REPO}/chapter-11/Data/transaksi_ml.csv"
copy "${OUT}/ch11_ml/transaksi_ml.json" \
     "${REPO}/chapter-11/Data/transaksi_ml.json"
copy "${OUT}/ch11_ml/pelanggan_agregat.json" \
     "${REPO}/chapter-11/Data/pelanggan_agregat.json"

# Sample JSON (100 baris pertama) untuk dokumentasi
if [[ -f "${OUT}/ch11_ml/transaksi_ml.json" ]]; then
  SAMPLE_DST="${REPO}/chapter-11/Data/transaksi_ml_sample.json"
  if [[ "${DRY}" == "1" ]]; then
    echo "[dry-run] sample 100 record -> ${SAMPLE_DST}"
  else
    "${ROOT}/.venv/bin/python" - <<PY
import json
from pathlib import Path
src = Path("${OUT}/ch11_ml/transaksi_ml.json")
dst = Path("${SAMPLE_DST}")
data = json.loads(src.read_text())
dst.write_text(json.dumps(data[:100], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"[sync] {dst} (100 record sample)")
PY
  fi
fi

# Bab 12 — Visualisasi (referensi lokal; pipeline lab tetap generate ke HDFS)
GOLD12="${REPO}/chapter-12/Konfigurasi-lab/data"
copy "${OUT}/ch12_viz/silver_transaksi.csv" "${GOLD12}/silver_transaksi.csv"
for g in tren_bulanan omzet_kelas omzet_geografis segmentasi_rfm tren_lanjutan; do
  copy "${OUT}/ch12_viz/gold_${g}.csv" "${GOLD12}/gold_${g}.csv"
done

# Bab 14 — Pipeline E2E
GOLD14="${REPO}/chapter-14/Konfigurasi-lab/data"
copy "${OUT}/ch14_e2e/silver_transaksi.csv" "${GOLD14}/silver_transaksi.csv"
for g in tren_bulanan omzet_kelas omzet_geografis segmentasi_rfm tren_lanjutan; do
  copy "${OUT}/ch14_e2e/gold_${g}.csv" "${GOLD14}/gold_${g}.csv"
done

echo ""
echo "=== Sync selesai ==="
echo "Catatan:"
echo "  - Bab 9 Airflow: generate_data.py runtime tetap dipakai; transaksi_harian.csv sebagai referensi."
echo "  - Bab 12/14: silver/gold disalin sebagai referensi; pipeline HDFS tetap via script lab."
