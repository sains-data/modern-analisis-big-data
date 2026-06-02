# Latihan 4 — Benchmark Format & Pipeline End-to-End
**Chapter 8 · Struktur & Penyimpanan Big Data** | Estimasi waktu: **30 menit**

## Tujuan

- Membandingkan ukuran dan waktu baca CSV vs Parquet vs ORC
- Memahami manfaat format kolumnar pada HDFS
- Merangkum pipeline end-to-end Bab 8

## Prasyarat

- [ ] Latihan 1–3 selesai
- [ ] Data Silver tersedia

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input | `hdfs:///datalake/silver/transaksi/` |
| Output benchmark | `hdfs:///datalake/benchmark/` |
| Script | `Konfigurasi-lab/app/format_benchmark.py` |

## Langkah Kerja

### 1) Tinjau skrip benchmark

Buka `Konfigurasi-lab/app/format_benchmark.py`.

### 2) Jalankan

```bash
cd sesi-praktikum/chapter-8/Konfigurasi-lab
bash scripts/run_format_benchmark.sh
```

## Tabel Pencatatan

| Format | Ukuran HDFS | Waktu (s) | Rasio vs CSV |
|---|---|---|---|
| CSV | | | 1.0× |
| Parquet | | | |
| ORC | | | |

## Ringkasan Pipeline

```text
Bronze (CSV HDFS) → Spark ETL → Silver (Parquet)
       → Hive external table → Query SQL
       → Spark agregasi → HBase profil_pelanggan
```

## Refleksi Singkat

1. Mengapa Parquet/ORC lebih kecil dari CSV?
2. Kapan ORC lebih disarankan daripada Parquet?

---

*Latihan 4 selesai. Lanjut ke **Latihan 5 — Eksplorasi Mandiri**.*
