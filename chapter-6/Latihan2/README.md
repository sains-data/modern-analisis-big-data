# Latihan 2 — Pipeline Bronze ke Silver
**Chapter 6 · Spark SQL & Medallion** | Estimasi waktu: **40 menit**

## Tujuan

- Membersihkan data Bronze dengan skema eksplisit
- Menerapkan deduplikasi, casting, standarisasi, dan validasi bisnis
- Menyimpan Silver sebagai Parquet terpartisi (`tahun`, `bulan`)

## Prasyarat

- [ ] Latihan 1 selesai — data Bronze ada di `/datalake/bronze/transaksi/`

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input | `hdfs:///datalake/bronze/transaksi/` |
| Output | `hdfs:///datalake/silver/transaksi/` |
| Script | `Konfigurasi-lab/app/pipeline_bronze_silver.py` |

## Langkah Kerja

### 1) Tinjau skrip pipeline

Buka dan pahami alur di `Konfigurasi-lab/app/pipeline_bronze_silver.py`:
- baca Bronze dengan `StructType` eksplisit
- dedup, cast, trim, validasi (`jumlah > 0`, `kuantitas > 0`)
- tulis Parquet terpartisi `tahun`, `bulan`

### 2) Jalankan pipeline (dari host)

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
bash scripts/run_pipeline_bronze_silver.sh
```

Pantau job di http://localhost:8088 dan http://localhost:4040.

### 3) Verifikasi Silver

```bash
bash scripts/spark_exec.sh "hdfs dfs -ls -R /datalake/silver/transaksi/"
bash scripts/spark_exec.sh "hdfs dfs -du -h /datalake/silver/transaksi/"
```

## Hasil yang Dicatat

- Jumlah baris Bronze vs baris valid Silver
- Baris yang ditolak beserta alasan (TRX011, TRX012, duplikat TRX001)
- Struktur sub-direktori `tahun=.../bulan=...`

## Refleksi Singkat

1. Dari 15 baris Bronze, berapa yang lolos validasi?
2. Mengapa `StructType` lebih baik dari `inferSchema=True` di produksi?

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Pipeline Silver ke Gold**.*
