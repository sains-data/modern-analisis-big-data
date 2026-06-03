#!/usr/bin/env bash
cd "$(dirname "${BASH_SOURCE[0]}")" && docker compose down 2>/dev/null || true
