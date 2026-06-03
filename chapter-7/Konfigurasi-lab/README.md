# Konfigurasi Lab Chapter 7

Praktik **Medallion Architecture berbasis Apache Arrow** di Python lokal (PyArrow → DuckDB → Polars). Tanpa klaster Spark/Hadoop.

Dataset **identik Bab 6** — entitas sintesis `catatan_aktivitas` + `entitas_partisipan`. Detail: [KATALOG-DATA.md](KATALOG-DATA.md).

## Referensi Lingkungan

| Item | Nilai |
|---|---|
| Python | 3.10+ (disarankan 3.11) |
| PyArrow | `>=14` |
| DuckDB | `>=0.10` |
| Polars | `>=0.20` |
| Root lab | folder `Konfigurasi-lab/` |
| Data mentah | `data/` |
| Datalake lokal | `datalake/` |

## Struktur folder

```
Konfigurasi-lab/
├── setup.sh
├── requirements.txt
├── KATALOG-DATA.md
├── data/
│   ├── transaksi.csv           ← 16 baris (legacy)
│   ├── pelanggan.csv           ← 7 baris
│   ├── catatan_aktivitas.csv   ← schema kanonik
│   └── entitas_partisipan.csv
├── app/
│   ├── paths.py
│   ├── bronze_arrow.py
│   ├── silver_arrow.py
│   ├── gold_arrow.py
│   └── validasi_pipeline.py
├── datalake/
│   ├── bronze/transaksi/
│   ├── silver/transaksi/
│   └── gold/
└── scripts/
    ├── run_bronze.sh … run_pipeline.sh
    └── verify_datalake.sh
```

## Volume harapan

| Layer | Baris |
|-------|-------|
| CSV `transaksi.csv` | 16 |
| Bronze Parquet | 15 |
| Silver | **12** |
| Pelanggan | 7 |

## Setup pertama kali

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
chmod +x setup.sh scripts/*.sh
bash setup.sh
bash scripts/setup_dirs.sh
bash scripts/verify_deps.sh
```

## Urutan latihan

| Perintah | Latihan | Engine |
|---|---|---|
| `bash scripts/run_bronze.sh` | 2 | PyArrow |
| `bash scripts/run_silver.sh` | 3 | DuckDB |
| `bash scripts/run_gold.sh` | 4 | Polars |
| `bash scripts/run_validasi.sh` | 5 | DuckDB audit |
| `bash scripts/run_pipeline.sh` | 2–5 (end-to-end) | semua |

```bash
bash scripts/verify_datalake.sh
```

## Regenerasi data sintesis

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch06_medallion
bash scripts/sync_to_chapters.sh
```

## Prasyarat konsep

- Bab 6: konsep Medallion + anomali dataset (volume Silver 12 baris)
- Bab 7: format kolumnar Arrow, zero-copy, lazy evaluation

## Troubleshooting

| Gejala | Solusi |
|---|---|
| Silver ≠ 12 baris | Regenerasi sync; reset `datalake/` lalu `run_pipeline.sh` |
| Bronze ≠ 15 baris | Pastikan CSV 16 baris; dedup TRX001 di Bronze |
| Omzet Silver ≠ Gold | Jalankan ulang `run_gold.sh` setelah Silver stabil |
