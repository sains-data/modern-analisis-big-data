#!/usr/bin/env bash
set -euo pipefail
CASE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="$(dirname "${BASH_SOURCE[0]}")/_py.sh"
mkdir -p "${CASE_ROOT}/data"/{sumber,bronze,silver,gold}
"${PY}" "${CASE_ROOT}/data/scripts/generate_konsesi_gambut.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_firms_hotspot.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_komponen_risiko.py"
"${PY}" "${CASE_ROOT}/data/scripts/generate_ispu_ispa.py"
