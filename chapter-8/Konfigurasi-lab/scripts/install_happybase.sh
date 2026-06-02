#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${SCRIPT_DIR}/spark_exec.sh" "
  pip install -q happybase 2>/dev/null || pip3 install -q happybase
  python3 -c 'import happybase; print(\"[OK] happybase\", happybase.__version__)'
"
