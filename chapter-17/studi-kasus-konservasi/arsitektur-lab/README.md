# Arsitektur Lab — Studi Kasus Konservasi

Lingkungan **cloud + edge** untuk pemantauan Kawasan Ekosistem Leuser: Kafka, Sedona/Airflow, MinIO/Iceberg, dan node tepi di stasiun lapangan.

## Isi yang direncanakan (Lampiran)

```
arsitektur-lab/
├── docker-compose.yml      # cloud stack
├── edge/                   # ARM SBC, model YOLO + CNN audio
├── kafka/
├── airflow/dags/
└── minio/
```

## Dokumentasi

→ **[PANDUAN-ARSITEKTUR-LAB.md](PANDUAN-ARSITEKTUR-LAB.md)**

## Prasyarat

- Bab 16 (Sedona spasial)  
- RAM cloud ≥ 16 GB; edge device terpisah untuk simulasi  

## Rujukan

`chapter-17.tex` — §Studi Kasus Konservasi, Gambar arsitektur KEL + edge.
