#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=scripts/_env.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"

python -c "
import pyarrow as pa
import duckdb
import polars as pl
print('PyArrow', pa.__version__)
print('DuckDB', duckdb.__version__)
print('Polars', pl.__version__)
print('[OK] Semua dependensi terpasang')
"

wc -l ../data/*.csv
