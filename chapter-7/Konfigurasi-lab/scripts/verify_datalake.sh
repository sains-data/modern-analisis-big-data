#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Bronze ==="
find "${LAB_ROOT}/datalake/bronze" -name "*.parquet" 2>/dev/null || echo "(kosong)"

echo ""
echo "=== Silver (partisi) ==="
find "${LAB_ROOT}/datalake/silver" -name "*.parquet" 2>/dev/null | head -15 || echo "(kosong)"

echo ""
echo "=== Gold ==="
ls -la "${LAB_ROOT}/datalake/gold/" 2>/dev/null || echo "(kosong)"
