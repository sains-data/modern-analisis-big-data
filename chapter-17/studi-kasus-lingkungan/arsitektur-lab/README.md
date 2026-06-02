# Arsitektur Lab — Studi Kasus Lingkungan

Folder untuk **lingkungan komputasi** monitoring karhutla Riau: ingest multi-sumber (FIRMS, Sentinel-2, KLHK, Dinkes), lakehouse Iceberg, dan orkestrasi batch/streaming.

## Isi yang direncanakan (Lampiran)

```
arsitektur-lab/
├── docker-compose.yml
├── .env.example
├── kafka/                    # hotspot.firms.riau, ispa.kecamatan.riau
├── airflow/dags/             # karhutla_riau_daily (02:00 WIB)
└── spark/                    # Structured Streaming
```

## Dokumentasi

→ **[PANDUAN-ARSITEKTUR-LAB.md](PANDUAN-ARSITEKTUR-LAB.md)**

## Prasyarat host

- Docker ≥ 24, RAM ≥ 16 GB  
- Akun Copernicus (Sentinel-2) dan FIRMS API key untuk data produksi  

## Rujukan buku

`chapter-17.tex` — §Studi Kasus Lingkungan, **Arsitektur Sistem** (Gambar lima lapisan karhutla).
