#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "${SCRIPT_DIR}/install_happybase.sh"
bash "${SCRIPT_DIR}/run_spark_submit.sh" spark_ke_hbase.py
