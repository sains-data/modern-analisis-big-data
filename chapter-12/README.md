# Chapter 12 — Visualisasi dan Eksplorasi Data

Praktik **pipeline visualisasi**: Spark → HDFS Gold → PostgreSQL → **Apache Superset** (5 tahap sesuai buku).

## Alur cepat

```bash
cd sesi-praktikum/chapter-12/Konfigurasi-lab
cp .env.example .env
bash start-viz.sh
bash build-spark.sh && bash start-spark.sh
bash scripts/run_pipeline_spark.sh
bash scripts/run_ekspor_postgresql.sh
bash scripts/verify_postgres.sh
# Buka http://localhost:8088 — latihan Superset (Tahap 3–5)
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan ↔ Tahap buku

| Latihan | Tahap buku | Topik |
|---|---|---|
| [Latihan 1](Latihan1/README.md) | Tahap 1 | Docker Superset+PG, `buat_data_viz.py` |
| [Latihan 2](Latihan2/README.md) | Tahap 2 | `persiapan_analitik.py`, `metrik_lanjutan.py`, ekspor JDBC |
| [Latihan 3](Latihan3/README.md) | Tahap 3 | Chart di Superset (Bar, Line, Big Number, Table) |
| [Latihan 4](Latihan4/README.md) | Tahap 4 | Dashboard `Analitik E-Commerce 2024` + Native Filter |
| [Latihan 5](Latihan5/README.md) | Tahap 5 | SQL Lab, tugas Growth Rate & Donut Chart |
