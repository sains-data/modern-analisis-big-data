# Modul 9 — Machine Learning Big Data

Gunakan setup baru di `Konfigurasi-lab/` agar environment, script, dan alur latihan konsisten.

## Alur Cepat

1. `cd Konfigurasi-lab`
2. Letakkan file binary:
   - `hadoop-3.4.1.tar.gz`
   - `spark-3.5.5-bin-hadoop3.tgz`
3. `bash build.sh` (sekali saat awal)
4. `bash start.sh`
5. `bash scripts/init_data.sh`
6. Kerjakan latihan berurutan: `Latihan1` → `Latihan5`

## Catatan Lingkungan

- Kontainer: `bigdata-spark`
- HDFS UI: http://localhost:9870
- YARN UI: http://localhost:8088
- Spark UI: http://localhost:4040 (aktif saat job berjalan)
- Semua script latihan sudah tersedia di `Konfigurasi-lab/scripts/`

Panduan lengkap ada di `Konfigurasi-lab/README.md`.
