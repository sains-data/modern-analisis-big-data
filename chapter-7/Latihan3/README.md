# Latihan 3 — Silver: Transformasi & Join dengan DuckDB
**Chapter 7 · Apache Arrow** | Estimasi waktu: **40 menit**

## Tujuan

- Membaca Parquet Bronze dan CSV partisipan ke Arrow (via DuckDB)
- Mendaftarkan Arrow Table sebagai view zero-copy (`con.register`)
- Menulis Silver sebagai Parquet terpartisi Hive (`tahun`, `bulan`)

## Prasyarat

- [ ] Latihan 2 selesai — Bronze **15 baris** di `batch_001.parquet`
- [ ] `data/pelanggan.csv` — **7 partisipan**

## Referensi volume harapan

| Tahap | Baris | Ditolak |
|-------|-------|---------|
| Bronze input | 15 | — |
| Silver output | **12** | TRX011, TRX012, TRX013 |
| % valid | 80% | 3 dari 15 |

Validasi SQL: `id_pelanggan` not null, `jumlah > 0`, `kuantitas > 0`, tanggal valid.  
TRX014 (`palembang`) **lolos** — `INITCAP` → `Palembang`.

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input Bronze | `datalake/bronze/transaksi/*.parquet` |
| Input dimensi | `data/pelanggan.csv` |
| Output | `datalake/silver/transaksi/` |
| Script | `Konfigurasi-lab/app/silver_arrow.py` |

## Langkah Kerja

### 1) Tinjau skrip Silver

`silver_arrow.py` — INNER JOIN pelanggan, `TRY_CAST` tanggal, `total_nilai = jumlah × kuantitas`.

### 2) Jalankan

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
bash scripts/run_silver.sh
```

Log harus menampilkan:

```json
{"baris_bronze": 15, "baris_silver": 12, "ditolak": 3, "pct_valid": 80.0}
```

### 3) Verifikasi partisi Silver

```bash
bash scripts/verify_datalake.sh
find datalake/silver/transaksi -name "*.parquet" | head
```

## Hasil yang Dicatat

- Bronze 15 → Silver **12** (bandingkan Bab 6: 16 → 12)
- Struktur `tahun=2024/bulan=.../`
- Contoh baris join: `nama_pelanggan`, `segmen`, `total_nilai`

## Refleksi Singkat

1. Apakah `con.register()` menyalin data atau zero-copy?
2. Mengapa hasil akhir Silver (12 baris) sama dengan Bab 6 meski dedup di tahap berbeda?

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Gold: Agregasi dengan Polars**.*
