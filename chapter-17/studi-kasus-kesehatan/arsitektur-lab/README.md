# Arsitektur Lab — Studi Kasus Kesehatan

Lingkungan untuk analitik **stunting Sumatera Utara**: ingest e-PPGBM (Kafka), batch bulanan (Airflow+Sedona), routing **OSRM**, lakehouse Iceberg.

## Isi yang direncanakan (Lampiran)

```
arsitektur-lab/
├── docker-compose.yml
├── kafka/                    # balita.upload.sumut, output.alert.kader
├── airflow/dags/             # stunting_sumut_monthly (tgl 5)
├── osrm/                     # graph Sumatera Utara
└── .env.example
```

## Dokumentasi

→ **[PANDUAN-ARSITEKTUR-LAB.md](PANDUAN-ARSITEKTUR-LAB.md)**

## Prasyarat

- RAM ≥ 16 GB (OSRM extract)  
- Bab 12 Superset opsional untuk Output 2  

## Rujukan

`chapter-17.tex` — §Studi Kasus Kesehatan, **Arsitektur Sistem**.
