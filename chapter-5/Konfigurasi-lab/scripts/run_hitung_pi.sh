#!/usr/bin/env bash
# SLICES=8 bash scripts/run_hitung_pi.sh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export SLICES="${SLICES:-4}"
export JUMLAH_DART="${JUMLAH_DART:-1000000}"
bash "${SCRIPT_DIR}/run_spark_submit.sh" hitung_pi.py "$@"
