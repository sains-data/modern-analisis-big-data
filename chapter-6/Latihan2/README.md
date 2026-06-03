# Latihan 2 — Pipeline Bronze ke Silver
**Chapter 6 · Spark SQL & Medallion** | Estimasi waktu: **40 menit**

## Tujuan

- Membersihkan data Bronze dengan skema eksplisit
- Menerapkan deduplikasi, casting, standarisasi, dan validasi bisnis
- Menyimpan Silver sebagai Parquet terpartisi (`tahun`, `bulan`)

## Prasyarat

- [ ] Latihan 1 selesai — **16 baris** Bronze di `/datalake/bronze/transaksi/`

## Referensi volume harapan

| Tahap | Baris | Keterangan |
|-------|-------|------------|
| Bronze (raw) | 16 | Termasuk duplikat TRX001 |
| Setelah dedup | 15 | TRX001 satu kali |
| Silver (valid) | **12** | TRX011, TRX012, TRX013 ditolak |
| Ditolak | 4 | 1 duplikat + 3 invalid |

Detail anomali: [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input | `hdfs:///datalake/bronze/transaksi/` |
| Output | `hdfs:///datalake/silver/transaksi/` |
| Script | `Konfigurasi-lab/app/pipeline_bronze_silver.py` |

## Langkah Kerja

### 1) Tinjau skrip pipeline

Alur `pipeline_bronze_silver.py`:
- baca Bronze dengan `StructType` eksplisit
- `dropDuplicates(["id_transaksi"])`
- standarisasi: `lower(kategori)`, `initcap(kota)` — TRX014 `palembang` → `Palembang`
- validasi: `id_pelanggan` not null, `jumlah > 0`, `kuantitas > 0`
- kolom turunan: `total_nilai = jumlah × kuantitas`
- tulis Parquet partisi `tahun`, `bulan`

### 2) Jalankan pipeline

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
bash scripts/run_pipeline_bronze_silver.sh
```

Pantau job di http://localhost:8088 dan http://localhost:4040.

### 3) Verifikasi Silver

```bash
bash scripts/spark_exec.sh "hdfs dfs -ls -R /datalake/silver/transaksi/"
```

Log pipeline harus menampilkan:

```
baris_masuk: 16
baris_valid: 12
baris_ditolak: 4
```

## Hasil yang Dicatat

- Jumlah baris Bronze (16) vs Silver (**12**)
- Baris ditolak: TRX011 (FK kosong), TRX012 (negatif), TRX013 (qty 0), + duplikat TRX001
- TRX014 lolos dengan kota `Palembang` setelah `initcap`
- Struktur partisi `tahun=2024/bulan=...`

## Refleksi Singkat

1. Dari 16 baris Bronze, mengapa hanya 12 yang lolos (bukan 15)?
2. Mengapa `StructType` lebih baik dari `inferSchema=True` di produksi?

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Pipeline Silver ke Gold**.*
