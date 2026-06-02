# Konfigurasi Lab Chapter 7

Praktik **Medallion Architecture berbasis Apache Arrow** di Python lokal (PyArrow → DuckDB → Polars). Tanpa klaster Spark/Hadoop.

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
├── data/
│   ├── transaksi.csv
│   └── pelanggan.csv
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
    ├── verify_deps.sh
    ├── setup_dirs.sh
    ├── run_bronze.sh
    ├── run_silver.sh
    ├── run_gold.sh
    ├── run_validasi.sh
    ├── run_pipeline.sh
    └── verify_datalake.sh
```

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
| `bash scripts/verify_deps.sh` | 1 | — |
| `bash scripts/run_bronze.sh` | 2 | PyArrow |
| `bash scripts/run_silver.sh` | 3 | DuckDB |
| `bash scripts/run_gold.sh` | 4 | Polars |
| `bash scripts/run_validasi.sh` | 5 | PyArrow + DuckDB |
| `bash scripts/run_pipeline.sh` | 2–5 (end-to-end) | semua |

Verifikasi output:

```bash
bash scripts/verify_datalake.sh
```

## Prasyarat konsep

- Chapter 6: dataset transaksi/pelanggan dan konsep Medallion
- Chapter 7: format kolumnar Arrow, zero-copy, lazy evaluation
