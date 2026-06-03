# Latihan 2 — Bronze: Ingest & Validasi dengan PyArrow
**Chapter 7 · Apache Arrow** | Estimasi waktu: **35 menit**

## Tujuan

- Membaca CSV langsung ke Arrow Table (kolumnar)
- Melakukan deduplikasi dan pengecekan null secara vectorized
- Menulis Bronze ke Parquet dengan statistik

## Prasyarat

- [ ] Latihan 1 selesai — **16 baris** di `data/transaksi.csv`

## Referensi volume harapan

| Tahap | Baris |
|-------|-------|
| CSV input | 16 |
| Bronze Parquet (setelah dedup) | **15** |
| Duplikat dihapus | 1 (TRX001) |

Di Bab 6, dedup dilakukan di Silver; di Bab 7 dedup di **Bronze** (`group_by id_transaksi`).

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input | `Konfigurasi-lab/data/transaksi.csv` |
| Output | `datalake/bronze/transaksi/batch_001.parquet` |
| Script | `Konfigurasi-lab/app/bronze_arrow.py` |

## Langkah Kerja

### 1) Tinjau skrip Bronze

Buka `bronze_arrow.py` — `read_csv`, `group_by` dedup, `write_statistics=True`.

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
print('Baris:', t.num_rows, '(harapan 15)')
print(t.schema)
"
```

## Hasil yang Dicatat

- Baris sebelum dedup: **16** · sesudah: **15**
- Null `id_pelanggan`: **1** (TRX011)
- Ukuran file Parquet Bronze

## Refleksi Singkat

1. Mengapa dedup di Bronze mengubah perhitungan rejection di Silver vs Bab 6?
2. Apa manfaat `write_statistics=True` pada Parquet?

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Silver: Transformasi dengan DuckDB**.*
