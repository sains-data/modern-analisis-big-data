#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "${LAB_ROOT}/datalake/bronze/transaksi"
mkdir -p "${LAB_ROOT}/datalake/silver/transaksi"
mkdir -p "${LAB_ROOT}/datalake/gold"
echo "[OK] Struktur datalake/"
ls -la "${LAB_ROOT}/datalake/"
