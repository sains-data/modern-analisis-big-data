#!/usr/bin/env bash
# Daftarkan koneksi Spark/Hive setelah Airflow init (dipanggil dari airflow-init)
set -euo pipefail

airflow connections delete spark_default 2>/dev/null || true
airflow connections add spark_default \
  --conn-type spark \
  --conn-host yarn \
  --conn-extra '{
    "deploy-mode": "client",
    "spark-home": "/opt/spark",
    "spark-binary": "/opt/airflow/scripts/spark_submit_bigdata.sh",
    "queue": "default"
  }'

airflow connections delete hive_default 2>/dev/null || true
airflow connections add hive_default \
  --conn-type hive_metastore \
  --conn-host host.docker.internal \
  --conn-port 10000 \
  --conn-login hive \
  --conn-password hive

airflow connections delete hiveserver2_default 2>/dev/null || true
airflow connections add hiveserver2_default \
  --conn-type hiveserver2 \
  --conn-host host.docker.internal \
  --conn-port 10000 \
  --conn-login hive \
  --conn-password hive

echo "[OK] Koneksi spark_default, hive_default, hiveserver2_default terdaftar."
