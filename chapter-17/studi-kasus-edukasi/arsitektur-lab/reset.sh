#!/usr/bin/env bash
cd "$(dirname "${BASH_SOURCE[0]}")"
docker compose down -v 2>/dev/null || true
CASE_ROOT="$(cd .. && pwd)"
rm -rf "${CASE_ROOT}/data"/{bronze,silver,gold}
rm -rf "${CASE_ROOT}/output"/output-*/*
