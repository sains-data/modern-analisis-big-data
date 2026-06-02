#!/usr/bin/env bash
set -euo pipefail

echo "=== Menjalankan kontainer bigdata-spark ==="
docker compose up -d
echo ""
echo "Tunggu 30–60 detik hingga Hadoop dan YARN aktif."
echo "Cek log: docker exec bigdata-spark cat /tmp/bootstrap.log"
echo ""
echo "UI:"
echo "  HDFS Web UI : http://localhost:9870"
echo "  YARN UI     : http://localhost:8088"
echo "  Spark UI    : http://localhost:4040 (saat job berjalan)"
