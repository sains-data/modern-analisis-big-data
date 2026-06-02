# Chapter 7 — Apache Arrow & Medallion Lokal

Praktik pipeline **Bronze → Silver → Gold** dengan **PyArrow**, **DuckDB**, dan **Polars** (tanpa YARN/Spark).

## Alur cepat

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
bash setup.sh
bash scripts/run_pipeline.sh
bash scripts/verify_datalake.sh
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | venv, data, struktur datalake |
| [Latihan 2](Latihan2/README.md) | `bronze_arrow.py` — PyArrow |
| [Latihan 3](Latihan3/README.md) | `silver_arrow.py` — DuckDB |
| [Latihan 4](Latihan4/README.md) | `gold_arrow.py` — Polars |
| [Latihan 5](Latihan5/README.md) | `validasi_pipeline.py` — audit |
