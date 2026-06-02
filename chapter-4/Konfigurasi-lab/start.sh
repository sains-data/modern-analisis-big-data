#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

bash scripts/ensure_hadoop_repo.sh || true
# shellcheck source=/dev/null
source "${ROOT_DIR}/.env" 2>/dev/null || true
HADOOP_REPO_DIR="${HADOOP_REPO_DIR:-${ROOT_DIR}/vendor/bigdata-hadoop}"

if [ ! -f "${HADOOP_REPO_DIR}/hadoop-3.4.1.tar.gz" ]; then
  echo "[ERROR] hadoop-3.4.1.tar.gz belum ada. Lihat pesan ensure_hadoop_repo.sh"
  exit 1
fi

echo "=== Start kontainer bigdata-hadoop ==="
(cd "${HADOOP_REPO_DIR}" && bash start.sh)

sleep 5
bash scripts/verify_cluster.sh || echo "[INFO] Verifikasi gagal — tunggu bootstrap lalu jalankan: bash scripts/verify_cluster.sh"

echo ""
echo "[OK] Klaster aktif."
echo "  Login shell : bash login.sh"
echo "  NameNode UI : http://localhost:9870"
echo "  YARN UI     : http://localhost:8088"
