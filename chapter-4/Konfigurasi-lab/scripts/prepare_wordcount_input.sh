#!/usr/bin/env bash
# Latihan 4 (bagian 1): upload dataset WordCount ke HDFS
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/copy_lab_data.sh"

bash "${SCRIPT_DIR}/hadoop_exec.sh" "
  hdfs dfs -mkdir -p /user/latihan/input
  hdfs dfs -put -f /tmp/dataset_wordcount.txt /user/latihan/input/
  hdfs dfs -ls /user/latihan/input/
  hdfs dfs -cat /user/latihan/input/dataset_wordcount.txt
"

echo "[OK] Input WordCount siap di /user/latihan/input/"
