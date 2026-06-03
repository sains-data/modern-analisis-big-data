# Chapter 11 — Machine Learning Big Data

Praktik **Spark MLlib** pada klaster HDFS + YARN: regresi, klasifikasi, K-Means, dan pipeline ML end-to-end.

Dataset **`transaksi_ml`** (10.000 baris, 200 partisipan) dihasilkan generator sintesis [`synthetic-data/`](../synthetic-data/README.md) — entitas `catatan_aktivitas` dengan label derivasi `segmen`.

## Alur Cepat

1. `cd Konfigurasi-lab`
2. Letakkan file binary:
   - `hadoop-3.4.1.tar.gz`
   - `spark-3.5.5-bin-hadoop3.tgz`
3. `bash build.sh` (sekali saat awal)
4. `bash start.sh`
5. `bash scripts/init_data.sh`
6. Kerjakan latihan berurutan: `Latihan1` → `Latihan5`

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)** · **[KATALOG-DATA.md](Konfigurasi-lab/KATALOG-DATA.md)**

## Data latihan

| File | Volume | Catatan |
|------|--------|---------|
| `Data/transaksi_ml.csv` / `.json` | **10.000** | Referensi statis (copula) |
| `Data/pelanggan_agregat.json` | **200** | Fitur K-Means Latihan 3 |
| HDFS Silver | **10.000** | Runtime via `init_data.sh` |

Label `segmen`: rendah / menengah / tinggi dari `total_nilai`.

## Catatan Lingkungan

- Kontainer: `bigdata-spark`
- HDFS UI: http://localhost:9870
- YARN UI: http://localhost:8088
- Spark UI: http://localhost:4040 (aktif saat job berjalan)
- Semua script latihan ada di `Konfigurasi-lab/scripts/`

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | Persiapan data & eksplorasi |
| [Latihan 2](Latihan2/README.md) | Regresi & klasifikasi |
| [Latihan 3](Latihan3/README.md) | K-Means clustering |
| [Latihan 4](Latihan4/README.md) | Pipeline ML end-to-end |
| [Latihan 5](Latihan5/README.md) | Eksplorasi hyperparameter |
