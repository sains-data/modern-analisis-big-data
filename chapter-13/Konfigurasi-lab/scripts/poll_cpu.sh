#!/usr/bin/env bash
# Polling CPU via Prometheus API — Bab 13 Tahap 4
set -euo pipefail

QUERY='100-(avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))*100)'

while true; do
  echo -n "$(date '+%H:%M:%S') CPU: "
  curl -sG "http://localhost:9090/api/v1/query" \
    --data-urlencode "query=${QUERY}" \
    | python3 -c "
import json, sys
d = json.load(sys.stdin)
r = d.get('data', {}).get('result', [])
if r:
    print(round(float(r[0]['value'][1]), 1), '%')
else:
    print('N/A')
" 2>/dev/null || echo "N/A"
  sleep 10
done
