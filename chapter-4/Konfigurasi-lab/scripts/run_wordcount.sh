#!/usr/bin/env bash
# Latihan 4 (bagian 2): jalankan MapReduce WordCount
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/hadoop_exec.sh" "
  set -e
  if hdfs dfs -test -d /user/latihan/output 2>/dev/null; then
    echo '[ERROR] /user/latihan/output sudah ada. Hapus dulu:'
    echo '  bash scripts/hdfs_management.sh   (atau hdfs dfs -rm -r ...)'
    exit 1
  fi
  JAR=\$(ls \$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar | head -1)
  echo \"Menggunakan JAR: \$JAR\"
  hadoop jar \"\$JAR\" wordcount /user/latihan/input /user/latihan/output
  echo '=== output ==='
  hdfs dfs -ls /user/latihan/output/
  hdfs dfs -cat /user/latihan/output/part-r-00000
"

echo "[OK] WordCount selesai. Pantau YARN: http://localhost:8088"
