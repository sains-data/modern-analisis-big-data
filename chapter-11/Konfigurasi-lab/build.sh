#!/usr/bin/env bash
set -euo pipefail

echo "=== Membangun Docker image bigdata-spark ==="
echo "Pastikan hadoop-3.4.1.tar.gz dan spark-3.5.5-bin-hadoop3.tgz"
echo "sudah ada di folder Konfigurasi-lab/ sebelum melanjutkan."
echo ""

if [ ! -f hadoop-3.4.1.tar.gz ]; then
  echo "[ERROR] hadoop-3.4.1.tar.gz tidak ditemukan!"
  echo "Unduh: https://archive.apache.org/dist/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz"
  exit 1
fi

if [ ! -f spark-3.5.5-bin-hadoop3.tgz ]; then
  echo "[ERROR] spark-3.5.5-bin-hadoop3.tgz tidak ditemukan!"
  echo "Unduh: https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz"
  exit 1
fi

docker compose build
echo ""
echo "[OK] Build selesai. Jalankan: bash start.sh"
