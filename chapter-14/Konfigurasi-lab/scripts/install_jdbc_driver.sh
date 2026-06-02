#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CH12="$(cd "${SCRIPT_DIR}/../../../chapter-12/Konfigurasi-lab" && pwd)/scripts/install_jdbc_driver.sh"
if [ -f "${CH12}" ]; then
  bash "${CH12}"
else
  bash "${SCRIPT_DIR}/spark_exec.sh" "
    mkdir -p /opt/spark/jars
    if [ ! -f /opt/spark/jars/postgresql-42.7.3.jar ]; then
      curl -fsSL -o /opt/spark/jars/postgresql-42.7.3.jar \
        https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
    fi
  "
fi
