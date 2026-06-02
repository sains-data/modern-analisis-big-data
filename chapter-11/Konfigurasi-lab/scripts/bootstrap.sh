#!/bin/bash
# Bootstrap: dijalankan otomatis saat kontainer start
set -e

LOG=/tmp/bootstrap.log
echo "[$(date)] Bootstrap dimulai..." | tee "$LOG"

service ssh start >> "$LOG" 2>&1
echo "[$(date)] SSH aktif" | tee -a "$LOG"

mkdir -p /opt/hdfs/namenode /opt/hdfs/datanode

$HADOOP_HOME/sbin/start-dfs.sh >> "$LOG" 2>&1
echo "[$(date)] HDFS aktif" | tee -a "$LOG"

$HADOOP_HOME/sbin/start-yarn.sh >> "$LOG" 2>&1
echo "[$(date)] YARN aktif" | tee -a "$LOG"

hdfs dfs -mkdir -p /spark-logs >> "$LOG" 2>&1

# Modul 9 — data lake ML
hdfs dfs -mkdir -p /datalake/bronze/transaksi >> "$LOG" 2>&1
hdfs dfs -mkdir -p /datalake/silver/transaksi >> "$LOG" 2>&1
hdfs dfs -mkdir -p /datalake/gold/prediksi_risiko >> "$LOG" 2>&1
hdfs dfs -mkdir -p /datalake/gold/prediksi_segmen >> "$LOG" 2>&1
hdfs dfs -mkdir -p /datalake/gold/segmentasi_pelanggan >> "$LOG" 2>&1
hdfs dfs -mkdir -p /feature_store/pelanggan_v1 >> "$LOG" 2>&1
hdfs dfs -mkdir -p /models/segmentasi_dt/v1 >> "$LOG" 2>&1
hdfs dfs -mkdir -p /models/klasifikasi_transaksi/v1 >> "$LOG" 2>&1

# Modul 7 — path latihan orkestrasi (shared container)
hdfs dfs -mkdir -p /datalake/bronze/latihan >> "$LOG" 2>&1
hdfs dfs -mkdir -p /datalake/silver/latihan >> "$LOG" 2>&1
hdfs dfs -mkdir -p /datalake/gold/latihan >> "$LOG" 2>&1

echo "[$(date)] Semua direktori HDFS siap" | tee -a "$LOG"
echo "[$(date)] Bootstrap selesai. Sistem siap." | tee -a "$LOG"

tail -f /dev/null
