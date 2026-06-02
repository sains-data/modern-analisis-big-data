#!/usr/bin/env bash
# Verifikasi daemon Hadoop (Latihan 1).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== docker ps ==="
docker ps --filter name=bigdata-hadoop --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

echo ""
echo "=== jps (di dalam kontainer) ==="
bash "${SCRIPT_DIR}/hadoop_exec.sh" "jps"

REQUIRED="NameNode DataNode ResourceManager NodeManager SecondaryNameNode"
MISSING=0
for proc in $REQUIRED; do
  if ! bash "${SCRIPT_DIR}/hadoop_exec.sh" "jps" 2>/dev/null | grep -q "${proc}"; then
    echo "[MISSING] ${proc}"
    MISSING=1
  else
    echo "[OK] ${proc}"
  fi
done

if [ "${MISSING}" -eq 1 ]; then
  exit 1
fi

echo ""
echo "[OK] Klaster Hadoop siap."
echo "  NameNode UI : http://localhost:9870"
echo "  YARN UI     : http://localhost:8088"
