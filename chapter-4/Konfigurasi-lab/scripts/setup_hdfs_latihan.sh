#!/usr/bin/env bash
# Latihan 3: buat direktori HDFS dan upload latihan.txt
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/copy_lab_data.sh"

bash "${SCRIPT_DIR}/hadoop_exec.sh" "
  hdfs dfs -mkdir -p /user/latihan
  hdfs dfs -put -f /tmp/latihan.txt /user/latihan/
  echo '=== ls /user/latihan ==='
  hdfs dfs -ls /user/latihan/
  echo '=== cat ==='
  hdfs dfs -cat /user/latihan/latihan.txt
  echo '=== fsck ==='
  hdfs fsck /user/latihan/latihan.txt -files -blocks -locations
  echo '=== dfsadmin -report (ringkas) ==='
  hdfs dfsadmin -report | head -30
"

echo "[OK] Setup HDFS latihan selesai."
