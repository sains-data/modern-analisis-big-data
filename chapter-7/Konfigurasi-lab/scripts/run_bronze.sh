#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=scripts/_env.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"
python bronze_arrow.py
