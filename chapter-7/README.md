# Chapter 7 — Apache Arrow & Medallion Lokal

Praktik pipeline **Bronze → Silver → Gold** dengan **PyArrow**, **DuckDB**, dan **Polars** (tanpa YARN/Spark).

Dataset **identik Bab 6** — generator sintesis [`synthetic-data/`](../synthetic-data/README.md), pipeline di filesystem lokal.

## Alur cepat

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
bash setup.sh
bash scripts/run_pipeline.sh
bash scripts/verify_datalake.sh
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)** · **[KATALOG-DATA.md](Konfigurasi-lab/KATALOG-DATA.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | venv, data, struktur datalake |
| [Latihan 2](Latihan2/README.md) | `bronze_arrow.py` — PyArrow |
| [Latihan 3](Latihan3/README.md) | `silver_arrow.py` — DuckDB |
| [Latihan 4](Latihan4/README.md) | `gold_arrow.py` — Polars |
| [Latihan 5](Latihan5/README.md) | `validasi_pipeline.py` — audit |

## Data latihan

| Tahap | Volume |
|-------|--------|
| CSV mentah | 16 baris transaksi + 7 pelanggan |
| Bronze Parquet | **15 baris** (dedup) |
| Silver | **12 baris** valid |
| Gold | agregat dari 12 baris |

Selaras entitas Bab 3–6: C001–C007 = PK-0001–PK-0007.

## Perbandingan Bab 6 vs Bab 7

| Aspek | Bab 6 | Bab 7 |
|-------|-------|-------|
| Engine | Spark on YARN | PyArrow + DuckDB + Polars |
| Storage | HDFS `/datalake/` | Lokal `datalake/` |
| Dedup | Silver | Bronze |
| Dataset | Sama (sintesis Copula) | Sama |
