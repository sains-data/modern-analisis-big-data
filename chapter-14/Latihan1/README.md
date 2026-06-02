# Latihan 1 — Pipeline ETL Medallion
**Chapter 14 · Pipeline Big Data End-to-End** | Estimasi: **40 menit** | **Tahap 1**

## Tujuan

- Menyiapkan klaster Spark + folder HDFS `/datalake/`
- Menjalankan pipeline Silver → Gold (`pipeline_ecommerce.py`)
- Memverifikasi tabel Gold: `tren_bulanan`, `omzet_kategori`, `segmentasi_rfm`

## Prasyarat

- [ ] [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Docker + tarball `bigdata-spark` (lihat Chapter 12)

## Referensi buku

- Skrip: `Konfigurasi-lab/app/pipeline_ecommerce.py`
- Silver: `hdfs:///datalake/silver/transaksi/`
- Gold: `hdfs:///datalake/gold/{tren_bulanan,omzet_kategori,segmentasi_rfm,omzet_kota}/`

## Langkah kerja

### 1) Spark

```bash
cd sesi-praktikum/chapter-14/Konfigurasi-lab
cp .env.example .env
bash build-spark.sh
bash start-spark.sh
bash scripts/spark_exec.sh "jps"
```

### 2) HDFS + pipeline lengkap

```bash
bash scripts/setup_hdfs_datalake.sh
bash scripts/run_pipeline_full.sh
```

> Silver sudah dari Bab 12? Jalankan hanya `bash scripts/run_pipeline_ecommerce.sh`.

### 3) Verifikasi

```bash
bash scripts/verify_hdfs.sh
```

Isi tabel observasi (buku §14.2.1):

| Layer | Baris | Ukuran |
|---|---|---|
| Silver | ~15.000 | |
| Gold: tren_bulanan | 12 | |
| Gold: omzet_kategori | 5 | |
| Gold: segmentasi_rfm | ~300 | |

Preview MoM di log Spark: kolom `mom_growth` per `periode`.

## Refleksi

1. Mengapa Bab 14 membaca Silver langsung, bukan landing JSON Bronze?
2. Apa perbedaan `mom_growth` di Gold vs metrik di Bab 12?

---

*Lanjut **Latihan 2 — Analitik DuckDB (Tahap 2)**.*
