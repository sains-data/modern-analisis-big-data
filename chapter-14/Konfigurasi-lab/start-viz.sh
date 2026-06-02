#!/usr/bin/env bash
set -euo pipefail
CH12="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../chapter-12/Konfigurasi-lab" && pwd)"
exec bash "${CH12}/start-viz.sh"
