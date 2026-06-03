# Konfigurasi Lab Chapter 11

Stack ini menyiapkan satu kontainer `bigdata-spark` untuk HDFS + YARN + Spark MLlib, lalu menjalankan script latihan dari folder repo.

Dataset referensi **10.000 transaksi ML** dari generator [`synthetic-data/`](../../synthetic-data/README.md) (Gaussian Copula). Detail mapping: **[KATALOG-DATA.md](KATALOG-DATA.md)**.

> Runtime: `scripts/init_data.sh` memanggil `buat_data_ml.py` → HDFS Parquet (schema sama, distribusi uniform acak seed 42). File di `Data/` = referensi statis copula.

## 1) Prasyarat