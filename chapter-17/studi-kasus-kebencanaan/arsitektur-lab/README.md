# Arsitektur Lab — Studi Kasus Kebencanaan

Stack **Kafka + MinIO** + pipeline Python (geopandas) yang meniru logika Spark/Sedona Bab 17.

## Komponen

| Layanan | Port | Fungsi |
|---|---|---|
| Kafka | 9093 | Topik `sensor.tma.musi`, `alert.banjir.musi` |
| MinIO | 9030 / 9031 | Lakehouse (bucket `banjir-musi`) |
| Python venv | lokal | Batch, streaming replay, spatial join |

## Quick start

```bash
cd sesi-praktikum/chapter-17/studi-kasus-kebencanaan/arsitektur-lab
cp .env.example .env
chmod +x *.sh scripts/*.sh

# Tanpa Docker (hanya Python):
bash scripts/prepare_data.sh
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh

# Dengan Docker (Kafka + MinIO):
bash start.sh
```

## Urutan skrip

| Skrip | Fungsi |
|---|---|
| `scripts/prepare_data.sh` | Generator data sintetis DAS Musi |
| `scripts/init_kafka.sh` | Topik + publish sample TMA |
| `scripts/run_pipeline.sh` | Ingest → siaga → spatial → output 1–4 |
| `scripts/verify_stack.sh` | Cek artefak Gold & output |

## Streaming

```bash
# Setelah docker compose up:
KAFKA_BOOTSTRAP=localhost:9093 python analitik/streaming/tma_siaga_stream.py --source kafka
```

## Dokumentasi

→ [PANDUAN-ARSITEKTUR-LAB.md](PANDUAN-ARSITEKTUR-LAB.md)

## Catatan produksi

Skrip Python ini setara cuplikan **PySpark + Sedona** di buku. Untuk cluster produksi, porting ke `spark-submit` dan SQL di `analitik/sql/`.
