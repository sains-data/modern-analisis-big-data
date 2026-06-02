# Latihan 2 — Hive & Spark SQL
**Chapter 8 · Struktur & Penyimpanan Big Data** | Estimasi waktu: **40 menit**

## Tujuan

- ETL Bronze → Silver dengan PySpark
- Mendaftarkan external table Hive terpartisi Parquet
- Menjalankan query analitik di Hive Shell (partition pruning)

## Prasyarat

- [ ] Latihan 1 selesai — Bronze di HDFS

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input | `hdfs:///datalake/bronze/transaksi/` |
| Output Silver | `hdfs:///datalake/silver/transaksi/` |
| Hive DB | `datalake.transaksi` |
| Script | `Konfigurasi-lab/app/hive_etl.py` |

## Langkah Kerja

### 1) Tinjau skrip ETL

Buka `Konfigurasi-lab/app/hive_etl.py` — Silver Parquet + `CREATE EXTERNAL TABLE` + `MSCK REPAIR`.

### 2) Jalankan ETL (dari host)

```bash
cd sesi-praktikum/chapter-8/Konfigurasi-lab
bash scripts/run_hive_etl.sh
```

### 3) Eksplorasi Hive Shell

```bash
bash login.sh
hive
```

```sql
USE datalake;
SHOW TABLES;

SELECT kategori,
       SUM(total_nilai) AS omzet_total,
       COUNT(*) AS n_transaksi
FROM transaksi
GROUP BY kategori ORDER BY omzet_total DESC;

EXPLAIN
SELECT kota, AVG(total_nilai) AS rata
FROM transaksi
WHERE tahun = 2024 AND bulan = 6
GROUP BY kota;
```

Alternatif Beeline: `beeline -u jdbc:hive2://localhost:10001/ -n hive -p hive`

## Refleksi Singkat

1. Apa fungsi `MSCK REPAIR TABLE`?
2. Apakah `EXPLAIN` menunjukkan partition pruning?

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Eksplorasi HBase**.*
