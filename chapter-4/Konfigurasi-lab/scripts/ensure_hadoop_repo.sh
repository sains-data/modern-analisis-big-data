#!/usr/bin/env bash
# Clone github.com/sains-data/bigdata-hadoop jika belum ada.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [ -f "${LAB_ROOT}/.env" ]; then
  # shellcheck source=/dev/null
  source "${LAB_ROOT}/.env"
fi

HADOOP_REPO_DIR="${HADOOP_REPO_DIR:-${LAB_ROOT}/vendor/bigdata-hadoop}"

if [ ! -d "${HADOOP_REPO_DIR}/.git" ]; then
  echo "=== Clone bigdata-hadoop ==="
  mkdir -p "$(dirname "${HADOOP_REPO_DIR}")"
  git clone https://github.com/sains-data/bigdata-hadoop.git "${HADOOP_REPO_DIR}"
fi

export HADOOP_REPO_DIR
echo "[OK] Repo: ${HADOOP_REPO_DIR}"

if [ ! -f "${HADOOP_REPO_DIR}/hadoop-3.4.1.tar.gz" ]; then
  echo ""
  echo "[PERINGATAN] File hadoop-3.4.1.tar.gz belum ada di:"
  echo "  ${HADOOP_REPO_DIR}/"
  echo ""
  echo "Unduh dari:"
  echo "  https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz"
  echo ""
  echo "Lalu jalankan: bash build.sh"
  exit 1
fi
