# Latihan 3 — Silver: Transformasi & Join dengan DuckDB
**Chapter 7 · Apache Arrow** | Estimasi waktu: **40 menit**

## Tujuan

- Membaca Parquet Bronze dan CSV pelanggan ke Arrow (via DuckDB)
- Mendaftarkan Arrow Table sebagai view zero-copy (`con.register`)
- Menulis Silver sebagai Parquet terpartisi Hive (`tahun`, `bulan`)

## Prasyarat

- [ ] Latihan 2 selesai — Bronze Parquet tersedia
- [ ] `data/pelanggan.csv` tersedia

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input Bronze | `datalake/bronze/transaksi/*.parquet` |
| Input dimensi | `data/pelanggan.csv` |
| Output | `datalake/silver/transaksi/` |
| Script | `Konfigurasi-lab/app/silver_arrow.py` |

## Langkah Kerja

### 1) Tinjau skrip Silver

Buka `Konfigurasi-lab/app/silver_arrow.py` — SQL validasi, join pelanggan, partisi hive via `pyarrow.dataset.write_dataset`.

### 2) Jalankan

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
bash scripts/run_silver.sh
```

### 3) Verifikasi partisi Silver

```bash
bash scripts/verify_datalake.sh
find datalake/silver/transaksi -name "*.parquet" | head
```

## Hasil yang Dicatat

- Baris Bronze vs Silver dan persentase ditolak
- Struktur folder `tahun=.../bulan=.../`
- Contoh satu baris hasil join (nama + segmen)

## Refleksi Singkat

1. Apakah `con.register()` menyalin data atau zero-copy?
2. Mengapa `TRY_CAST` dipakai untuk tanggal?

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Gold: Agregasi dengan Polars**.*
