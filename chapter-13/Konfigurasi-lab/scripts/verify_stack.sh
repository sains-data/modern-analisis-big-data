#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "=== docker compose ps ==="
docker compose -f docker-compose-monitoring.yml ps

echo ""
echo "=== Prometheus targets ==="
curl -sf "http://localhost:9090/api/v1/targets" \
  | python3 -c "
import json, sys
for t in json.load(sys.stdin)['data']['activeTargets']:
    print(t['labels'].get('job','?'), t['health'])
" || echo "[ERROR] Prometheus tidak merespons di :9090"

echo ""
echo "=== Node Exporter (sample) ==="
curl -sf "http://localhost:9100/metrics" | head -3 || echo "[ERROR] :9100"

echo ""
echo "=== Alert rules ==="
curl -sf "http://localhost:9090/api/v1/rules" \
  | python3 -c "
import json, sys
groups = json.load(sys.stdin).get('data', {}).get('groups', [])
for g in groups:
    for r in g.get('rules', []):
        print(r.get('name', r.get('alert', '?')))
" 2>/dev/null || echo "(belum siap)"

echo ""
echo "=== Grafana ==="
curl -sf -o /dev/null -w "HTTP %{http_code}\n" http://localhost:3000/login || true

echo ""
echo "[OK] Verifikasi selesai. UI:"
echo "  Prometheus : http://localhost:9090"
echo "  Grafana    : http://localhost:3000 (admin/admin)"
echo "  Node export: http://localhost:9100/metrics"
