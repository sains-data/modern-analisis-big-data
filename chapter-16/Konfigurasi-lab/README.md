# Konfigurasi Lab Chapter 16

Lingkungan **modul-spasial** sesuai Bab 16: Spark cluster + **Apache Sedona Jupyter** + **MinIO** (GeoParquet / raw CSV).

## Layanan

| Kontainer | Image | Port (host) |
|---|---|---|
| `ch16-sedona-jupyter` | `apache/sedona:latest` | 8888, 4040 |
| `ch16-spark-master` | `bitnami/spark:3.5.5` | 8081, 7077 |
| `ch16-spark-worker` | `bitnami/spark:3.5.5` | — |
| `ch16-minio` | `minio/minio` | **9020**, **9021** |

| UI | URL | Kredensial |
|---|---|---|
| Jupyter | http://localhost:8888 | token `sedona123` |
| MinIO Console | http://localhost:9021 | minioadmin / minioadmin |
| Spark Master | http://localhost:8081 | — |

## Struktur

```
Konfigurasi-lab/
├── docker-compose.yml
├── notebooks/analitik_spasial.ipynb   # notebook utama (5 tahap)
├── data/                              # hotspot + batas kecamatan (generate)
├── output/{bronze,silver,gold}/       # hasil pipeline (volume mount)
└── scripts/
    ├── prepare_data.sh
    ├── init_minio.sh
    ├── download_data.sh              # FIRMS (opsional, butuh API key)
    └── verify_stack.sh
```

## Setup

```bash
cd sesi-praktikum/chapter-16/Konfigurasi-lab
cp .env.example .env
chmod +x start.sh stop.sh scripts/*.sh
bash start.sh
```

`start.sh` akan: `docker compose up`, generate 500 baris hotspot sintetis, GeoParquet batas kecamatan, upload ke bucket `geodata`, lalu `verify_stack.sh`.

## Data

| File | Sumber |
|---|---|
| `data/hotspot_sample.csv` | `scripts/generate_sample.py` |
| `data/hotspot_sumatera_2024.csv` | salinan nama buku (Tahap 1) |
| `data/batas_kecamatan_sumatera.geoparquet` | `scripts/generate_batas_kecamatan.py` |

Data FIRMS sungguhan (opsional):

```bash
# isi FIRMS_MAP_KEY di .env
bash scripts/download_data.sh
```

## Reset

```bash
bash reset.sh   # down -v, hapus output, start ulang
```

## Notebook

Jalankan sel berurutan di `notebooks/analitik_spasial.ipynb`:

1. Verifikasi Sedona  
2. Bronze/Silver hotspot  
3. Agregasi H3 → `output/gold/hotspot_h3/`  
4. Spatial join kecamatan  
5. Gi* + DBSCAN (Tahap 5)

Working directory Jupyter: `/home/jovyan/work` (path relatif `data/`, `output/`).

## Hentikan

```bash
bash stop.sh
```
