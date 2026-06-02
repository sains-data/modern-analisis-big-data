#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] python3 tidak ditemukan."
  exit 1
fi

version="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

if [[ "$version" != "3.10" && "$version" != "3.11" ]]; then
  echo "[ERROR] Python $version tidak cocok untuk pyspark==3.5.5."
  echo "        Gunakan Python 3.10 atau 3.11."
  exit 1
fi

echo "[OK] Python $version kompatibel."
