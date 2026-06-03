# Konfigurasi Lab Chapter 12

Pipeline **visualisasi end-to-end** sesuai Bab 12: Spark (HDFS Gold) → PostgreSQL → **Apache Superset**.

Dataset referensi **15.000 transaksi** + 5 tabel Gold dari generator [`synthetic-data/`](../../synthetic-data/README.md) (Gaussian Copula). Detail: **[KATALOG-DATA.md](KATALOG-DATA.md)**.

> Runtime: skrip Spark di `app/` menulis ke HDFS. File `data/*.csv` = referensi statis untuk inspeksi volume & schema.

## Komponen (sesuai buku)

| Komponen | Versi / nama |
|---|---|
| Docker Compose | `docker-compose-viz.yml` |
| PostgreSQL | 15 — kontainer `viz-postgres` |
| Apache Superset | 3.1.0 — kontainer `viz-superset` |
| Spark / Hadoop | `bigdata-spark` (vendor) |

> Bab 12 **tidak** memakai Prometheus/Grafana dalam sesi praktik. Fokus: Superset + PostgreSQL + Spark.

## Port

| Port | Layanan |
|---|---|
| 8088 | Superset UI (`admin` / `admin`) — hentikan klaster Spark jika port bentrok dengan YARN UI |
| 5432 | PostgreSQL (`superset` / `superset`, DB `analytics`) |
| 9870 | HDFS NameNode (klaster Spark) |

## Struktur

```
Konfigurasi-lab/
├── docker-compose-viz.yml
├── start-viz.sh / stop-viz.sh
├── start-spark.sh / stop-spark.sh / build-spark.sh
├── data/
│   ├── silver_transaksi.csv          # 15.000 baris
│   ├── gold_tren_bulanan.csv         # 12 bulan
│   ├── gold_tren_lanjutan.csv        # MA3, MoM
│   ├── gold_omzet_kelas.csv          # 6 kategori
│   ├── gold_omzet_geografis.csv      # 10 kota
│   └── gold_segmentasi_rfm.csv       # 300 partisipan
├── KATALOG-DATA.md
├── app/
│   ├── buat_data_viz.py          # 15.000 baris, 12 bulan
│   ├── persiapan_analitik.py     # Gold: tren_bulanan, omzet_*
│   ├── metrik_lanjutan.py        # MA3, MoM → tren_lanjutan
│   └── ekspor_postgresql.py      # JDBC → PostgreSQL
└── scripts/
    ├── run_pipeline_spark.sh
    ├── run_ekspor_postgresql.sh
    └── verify_postgres.sh
```

## Setup

```bash
cd sesi-praktikum/chapter-12/Konfigurasi-lab
cp .env.example .env
chmod +x *.sh scripts/*.sh

# 1) Stack visualisasi
bash start-viz.sh

# 2) Klaster Spark (tarball hadoop + spark di vendor/bigdata-spark/)
bash build-spark.sh
bash start-spark.sh

# 3) Pipeline data (Tahap 1–2 buku)
bash scripts/run_pipeline_spark.sh
bash scripts/run_ekspor_postgresql.sh   # viz-postgres harus sudah Up
bash scripts/verify_postgres.sh
```

## Tabel PostgreSQL (setelah ekspor)

| Tabel | Sumber HDFS | Perkiraan baris |
|---|---|---|
| `tren_bulanan` | `gold/tren_lanjutan/` | **12** (12 bulan 2024) |
| `omzet_kategori` | `gold/omzet_kategori/` | **6** kategori |
| `omzet_kota` | `gold/omzet_kota/` | **10** kota |

## JDBC dari Spark ke PostgreSQL

Kontainer `bigdata-spark` dan `viz-postgres` di jaringan Docker berbeda. Atur `PG_JDBC_URL` di `.env`:

- Mac/Windows: `jdbc:postgresql://host.docker.internal:5432/analytics`
- Linux: `jdbc:postgresql://172.17.0.1:5432/analytics` (atau IP dari `ip route | awk '/default/{print $3}'` di dalam kontainer)

## Hentikan

```bash
bash stop-viz.sh
bash stop-spark.sh
```
