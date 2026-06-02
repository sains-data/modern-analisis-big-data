#!/usr/bin/env bash
# Menjalankan stack Airflow + Atlas Chapter 9 (selaras Data-Lakehouse-Metadata)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "${SCRIPT_DIR}"

if [ -f .env ]; then
  set -a
  # shellcheck source=/dev/null
  source .env
  set +a
fi

export DOCKER_GID="${DOCKER_GID:-$(getent group docker 2>/dev/null | cut -d: -f3 || stat -c '%g' /var/run/docker.sock 2>/dev/null || echo 999)}"

echo "=== Chapter 9: build image Airflow ==="
docker compose build airflow-init airflow-webserver airflow-scheduler

echo "=== Chapter 9: infrastruktur Atlas (ZK, Kafka, HBase, Solr) ==="
docker compose up -d postgres zookeeper kafka
sleep 10
docker compose up -d hbase solr
sleep 20
docker compose up -d solr-atlas-init
sleep 10

echo "=== Chapter 9: Apache Atlas ==="
docker compose up -d atlas
echo "Atlas butuh 3–5 menit warmup pertama kali..."

echo "=== Chapter 9: Apache Airflow ==="
docker compose up -d airflow-init
sleep 15
docker compose up -d airflow-webserver airflow-scheduler

echo ""
echo "=== Status layanan ==="
docker compose ps

echo ""
echo "UI (dari browser host):"
echo "  Airflow  → http://localhost:${MOD7_AIRFLOW_WEB_PORT:-18681}  (airflow / airflow)"
echo "  Atlas    → http://localhost:${MOD7_ATLAS_PORT:-22100}        (admin / admin)"
echo ""
echo "Langkah berikutnya (jika bigdata-spark sudah jalan):"
echo "  bash scripts/setup_bigdata_spark.sh"
