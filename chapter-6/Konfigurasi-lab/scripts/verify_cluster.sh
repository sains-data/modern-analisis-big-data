#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== docker ps ==="
docker ps --filter name=bigdata-spark --format 'table {{.Names}}\t{{.Status}}'

echo ""
echo "=== jps ==="
bash "${SCRIPT_DIR}/spark_exec.sh" "jps"

REQUIRED="NameNode DataNode ResourceManager NodeManager SecondaryNameNode"
MISSING=0
JPS_OUT=$(bash "${SCRIPT_DIR}/spark_exec.sh" "jps" 2>/dev/null || true)
for proc in $REQUIRED; do
  if echo "${JPS_OUT}" | grep -q "${proc}"; then
    echo "[OK] ${proc}"
  else
    echo "[MISSING] ${proc}"
    MISSING=1
  fi
done

if [ "${MISSING}" -eq 1 ]; then
  echo "Cek bootstrap: bash scripts/spark_exec.sh 'tail -20 /tmp/bootstrap.log'"
  exit 1
fi

echo ""
echo "[OK] Klaster Hadoop-Spark siap."
echo "  NameNode : http://localhost:9870"
echo "  YARN     : http://localhost:8088"
echo "  Spark UI : http://localhost:4040 (saat job berjalan)"
