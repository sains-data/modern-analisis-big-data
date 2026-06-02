# Arsitektur Lab — Studi Kasus Kebencanaan

Folder ini akan menampung **konfigurasi lingkungan komputasi** untuk prototipe peringatan dini banjir DAS Musi: layanan Docker, topik Kafka, koneksi MinIO/Iceberg, dan parameter Spark Streaming.

## Isi yang direncanakan (Lampiran)

```
arsitektur-lab/
├── docker-compose.yml      # Kafka, Spark, Airflow, MinIO, GeoServer (opsional)
├── .env.example
├── kafka/                  # topik sensor.tma.musi
├── spark/                  # konfigurasi streaming
└── airflow/dags/           # batch harian Sedona + Sentinel-1
```

Saat ini hanya dokumentasi; file konfigurasi menyusul di Lampiran praktikum.

## Dokumentasi

→ **[PANDUAN-ARSITEKTUR-LAB.md](PANDUAN-ARSITEKTUR-LAB.md)** — diagram lapisan, pola Lambda, port layanan, checklist sprint 1.

## Prasyarat host

- Docker Engine ≥ 24, Compose ≥ 2.20  
- RAM ≥ 16 GB disarankan (Spark + Kafka + Jupyter/Sedona)  
- Port bebas: lihat tabel port di panduan detail  

## Rujukan buku

`chapter-17.tex` — §Studi Kasus Kebencanaan, subbab **Arsitektur Sistem** (Gambar pipeline banjir).
