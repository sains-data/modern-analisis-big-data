# Latihan 2 — Bronze: Ingest & Validasi dengan PyArrow
**Chapter 7 · Apache Arrow** | Estimasi waktu: **35 menit**

## Tujuan

- Membaca CSV langsung ke Arrow Table (kolumnar)
- Melakukan deduplikasi dan pengecekan null secara vectorized
- Menulis Bronze ke Parquet dengan statistik

## Prasyarat

- [ ] Latihan 1 selesai — `data/transaksi.csv` tersedia

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input | `Konfigurasi-lab/data/transaksi.csv` |
| Output | `datalake/bronze/transaksi/batch_001.parquet` |
| Script | `Konfigurasi-lab/app/bronze_arrow.py` |

## Langkah Kerja

### 1) Tinjau skrip Bronze

Buka `Konfigurasi-lab/app/bronze_arrow.py` — perhatikan `read_csv`, `group_by` dedup, dan `write_table` dengan `write_statistics=True`.

### 2) Jalankan

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
bash scripts/run_bronze.sh
```

### 3) Verifikasi Parquet Bronze

```bash
source .venv/bin/activate
cd app
python -c "
import pyarrow.parquet as pq
from paths import BRONZE_BATCH
t = pq.read_table(str(BRONZE_BATCH))
print(t.schema, t.num_rows)
"
```

## Hasil yang Dicatat

- Jumlah baris sebelum/sesudah dedup
- Null per kolom (terutama `id_pelanggan` untuk TRX011)
- Ukuran file Parquet Bronze

## Refleksi Singkat

1. Mengapa membaca CSV langsung ke Arrow lebih efisien daripada loop Python?
2. Apa manfaat `write_statistics=True` pada Parquet?

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Silver: Transformasi dengan DuckDB**.*
