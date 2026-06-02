#!/usr/bin/env bash
# Beban CPU 60 detik — Bab 13 Tahap 4 (alternatif jika `stress` tidak terpasang)
set -euo pipefail

CORES="${1:-2}"
SECONDS="${2:-60}"

if command -v stress >/dev/null 2>&1; then
  echo "[INFO] stress --cpu ${CORES} --timeout ${SECONDS}s"
  stress --cpu "${CORES}" --timeout "${SECONDS}s"
else
  echo "[INFO] Python CPU burn: ${CORES} thread, ${SECONDS}s"
  python3 - "${CORES}" "${SECONDS}" <<'PY'
import sys, threading, time

cores = int(sys.argv[1])
seconds = int(sys.argv[2])

def burn():
    end = time.time() + seconds
    while time.time() < end:
        _ = sum(range(1_000_000))

threads = [threading.Thread(target=burn) for _ in range(cores)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"[OK] Beban CPU selesai ({cores} thread, {seconds}s)")
PY
fi
