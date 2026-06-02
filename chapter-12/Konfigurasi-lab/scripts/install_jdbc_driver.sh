#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  if [ ! -f /opt/spark/jars/postgresql-42.7.3.jar ]; then
    wget -q -O /opt/spark/jars/postgresql-42.7.3.jar \
      https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
  fi
  ls -lh /opt/spark/jars/postgresql-42.7.3.jar
"
