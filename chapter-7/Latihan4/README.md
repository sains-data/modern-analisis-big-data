# Latihan 4 — Gold: Agregasi Bisnis dengan Polars
**Chapter 7 · Apache Arrow** | Estimasi waktu: **35 menit**

## Tujuan

- Membaca Silver dengan `scan_parquet` (lazy, hive partitioning)
- Membuat agregat Gold: per kategori, per segmen+waktu, top produk (window)
- Menulis Gold ke Parquet via konversi zero-copy Polars → Arrow

## Prasyarat

- [ ] Latihan 3 selesai — Silver terpartisi di `datalake/silver/transaksi/`

## Referensi data

- Silver: **12 baris** valid (sama Bab 6)
- Gold agregat dari 12 transaksi × 7 partisipan

## Referensi Lingkungan Lab

| Output | Path |
|---|---|
| Gold per kategori | `datalake/gold/per_kategori.parquet` |
| Gold per segmen | `datalake/gold/per_segmen.parquet` |
| Top produk | `datalake/gold/top_produk.parquet` |
| Script | `Konfigurasi-lab/app/gold_arrow.py` |

## Langkah Kerja

### 1) Tinjau skrip Gold

Buka `Konfigurasi-lab/app/gold_arrow.py` — lazy `scan_parquet`, agregasi, `rank().over("kategori")`, `collect()` lalu `to_arrow()` ke Parquet.

### 2) Jalankan

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
bash scripts/run_gold.sh
```

## Hasil yang Dicatat

- Tabel omzet per kategori (dicetak di terminal)
- Jumlah baris masing-masing file Gold
- Top 3 produk per kategori (dari `top_produk.parquet`)

## Refleksi Singkat

1. Kapan `collect()` memicu eksekusi — analogi dengan Spark `show()`?
2. Mengapa Polars cocok untuk lapisan Gold?

---

*Latihan 4 selesai. Lanjut ke **Latihan 5 — Validasi & Perbandingan Pipeline**.*
