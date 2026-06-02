#!/usr/bin/env bash
# Ekspor dashboard — Bab 13 Tahap 5 Tugas C
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${ROOT_DIR}/bigdata_dashboard_backup.json"
TITLE_FILTER="${1:-BigData}"

UID=$(curl -s -u admin:admin "http://localhost:3000/api/search" \
  | python3 -c "
import json, sys
title = sys.argv[1]
items = json.load(sys.stdin)
for x in items:
    if title in x.get('title', ''):
        print(x['uid'])
        break
" "${TITLE_FILTER}")

if [ -z "${UID}" ]; then
  echo "[ERROR] Dashboard dengan '${TITLE_FILTER}' di judul tidak ditemukan."
  exit 1
fi

curl -s -u admin:admin "http://localhost:3000/api/dashboards/uid/${UID}" \
  | python3 -m json.tool > "${OUT}"

python3 -c "
import json
d = json.load(open('${OUT}'))
print('Dashboard tersimpan:', '${OUT}')
print('Panels:', len(d.get('dashboard', {}).get('panels', [])))
"
