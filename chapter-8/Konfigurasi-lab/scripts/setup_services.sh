#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  set -e
  start-dfs.sh 2>/dev/null || true
  start-yarn.sh 2>/dev/null || true
  start-hbase.sh 2>/dev/null || true
  sleep 5

  if ! netstat -tulnp 2>/dev/null | grep -q ':9090'; then
    nohup hbase thrift start > /tmp/hbase-thrift.log 2>&1 &
    sleep 3
  fi

  if [ ! -f /tmp/.hive_schema_inited ]; then
    schematool -dbType derby -initSchema 2>/dev/null || true
    touch /tmp/.hive_schema_inited
  fi

  if ! jps | grep -q RunJar; then
    nohup hive --service metastore > /tmp/hive-metastore.log 2>&1 &
    sleep 5
  fi

  hive -e 'CREATE DATABASE IF NOT EXISTS datalake;' 2>/dev/null || true

  echo '=== Port Thrift HBase (9090) ==='
  netstat -tulnp 2>/dev/null | grep 9090 || echo '(belum terlihat — tunggu beberapa detik)'
  jps | grep -E 'HMaster|HRegion|RunJar' || true
"

echo "[OK] Layanan HBase Thrift & Hive disiapkan."
