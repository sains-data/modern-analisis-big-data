#!/usr/bin/env bash
set -euo pipefail
curl -X POST http://localhost:9090/-/reload
echo ""
echo "=== Alert rules terdaftar ==="
curl -s http://localhost:9090/api/v1/rules \
  | python3 -c "import json,sys; [print(r.get('name')) for g in json.load(sys.stdin).get('data',{}).get('groups',[]) for r in g.get('rules',[])]"
