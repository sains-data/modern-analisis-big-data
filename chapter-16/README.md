# Chapter 16 — Analitik Big Data Spasial

Praktik **pipeline geospasial Sumatera**: hotspot FIRMS → Medallion GeoParquet (Bronze/Silver/Gold) → grid **H3** → spatial join → **Getis-Ord Gi*** → eksplorasi **DBSCAN**, dengan **Apache Sedona** di Jupyter.

> **Chapter 15** tidak memiliki sesi praktikum; modul ini melanjutkan setelah Bab 14.

## Alur cepat

```bash
cd sesi-praktikum/chapter-16/Konfigurasi-lab
cp .env.example .env
chmod +x start.sh stop.sh reset.sh scripts/*.sh
bash start.sh
# Buka http://localhost:8888 — token: sedona123
# Notebook: notebooks/analitik_spasial.ipynb
bash stop.sh
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan ↔ Tahap buku

| Latihan | Tahap | Topik |
|---|---|---|
| [Latihan 1](Latihan1/README.md) | Setup + Tahap 1 | Docker, Sedona, Bronze/Silver |
| [Latihan 2](Latihan2/README.md) | Tahap 2 | Agregasi grid H3 |
| [Latihan 3](Latihan3/README.md) | Tahap 3 | Spatial join kecamatan |
| [Latihan 4](Latihan4/README.md) | Tahap 4 | Getis-Ord Gi* |
| [Latihan 5](Latihan5/README.md) | Tahap 5 | DBSCAN, physical plan, diskusi |

## Prasyarat

- Docker Engine ≥ 24, Compose ≥ 2.20
- RAM ≥ 8 GB (image `apache/sedona` ~3 GB unduhan pertama)
- Python 3.10+ di host (generate data GeoParquet)

## Catatan port

| Layanan | Port | Bentrok umum |
|---|---|---|
| Jupyter | 8888 | — |
| Spark UI (job) | 4040 | — |
| Spark Master UI | 8081 | — |
| MinIO API / Console | **9020** / **9021** | Ch.3 memakai 9000/9001 |
