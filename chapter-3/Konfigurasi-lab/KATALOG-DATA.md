# Katalog Data — Chapter 3

Dataset latihan **`sample_users.csv`** berasal dari generator sintesis Gaussian Copula (`synthetic-data/`), disinkronkan ke `raw-data/` via `synthetic-data/scripts/sync_to_chapters.sh`.

## File sumber

| Path | Format | Volume |
|------|--------|--------|
| `raw-data/sample_users.csv` | CSV | **51 baris** (+ header) |

## Schema

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `id` | integer | Identitas partisipan |
| `name` | string | Nama partisipan |
| `age` | integer | Usia (22–54) |
| `city` | string | Unit geografis (10 kota) |
| `salary` | float | Pendapatan bulanan (Rp); dapat null |
| `join_date` | date | Tanggal bergabung (`YYYY-MM-DD`) |

## Kota (`city`)

Jakarta · Surabaya · Bandung · Medan · Semarang · Makassar · Palembang · Denpasar · Yogyakarta · Balikpapan

## Anomali terkontrol (latihan data quality)

| # | Baris | Jenis | Detail |
|---|-------|-------|--------|
| 1 | 3 | Null | `Sari Dewi` — kolom `salary` kosong |
| 2 | 5 & 51 | Duplikat | `Maria Chen` — baris identik (duplikat penuh) |

Gunakan anomali ini saat Latihan 3 untuk memahami deduplikasi dan imputasi median.

## Hasil pipeline Medallion (harapan)

| Layer | Key | Volume |
|-------|-----|--------|
| Bronze | `bronze/users/sample_users.csv` | 51 baris |
| Silver | `silver/users/users_clean.parquet` | **50 baris** (setelah dedup) |
| Gold | `gold/summary/city_summary.parquet` | **10 baris** (satu per kota) |

Transformasi Silver (`transform.py`):
- `drop_duplicates()` — baris 51 dihapus
- `salary` null → diisi **median** gaji
- Kolom distandarisasi lowercase; `join_date` → datetime

Agregasi Gold (`aggregate.py`):
- `avg_salary`, `total_karyawan`, `avg_usia` per `city`

## Regenerasi data

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch03_minio
bash scripts/sync_to_chapters.sh
```

Seed default: `42` (reproduksibel).
