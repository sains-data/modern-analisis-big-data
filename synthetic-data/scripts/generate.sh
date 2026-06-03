#!/usr/bin/env bash
# Generate semua output data sintesis (Gaussian Copula).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ ! -d .venv ]]; then
  echo "[setup] Membuat virtualenv .venv ..."
  python3 -m venv .venv
fi

echo "[setup] Install dependensi ..."
.venv/bin/pip install -q -r requirements.txt

echo "[generate] Menjalankan copula_gaussian.py ..."
.venv/bin/python generators/copula_gaussian.py --module "${1:-all}" "${@:2}"

echo ""
echo "Selesai. Verifikasi: bash scripts/verify_outputs.sh"
echo "Sync ke lab:        bash scripts/sync_to_chapters.sh"
