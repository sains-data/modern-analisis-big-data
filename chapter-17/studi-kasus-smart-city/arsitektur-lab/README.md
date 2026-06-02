# Arsitektur Lab — Studi Kasus Smart City

Lingkungan **streaming-first** untuk integrasi CCTV (edge), GPS TMD, sensor udara, probe kendaraan, dan media sosial ke satu lakehouse.

## Isi yang direncanakan (Lampiran)

```
arsitektur-lab/
├── docker-compose.yml
├── kafka/                 # 5 topik + producer simulasi
├── spark/                 # Structured Streaming
├── edge/                  # detektor CCTV (opsional)
└── superset/              # dashboard ATCS / IQU
```

## Dokumentasi

→ **[PANDUAN-ARSITEKTUR-LAB.md](arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md)**

## Prasyarat

- Bab 9–10 (Kafka, Spark Streaming)  
- Bab 12 (Superset) untuk dashboard  

## Rujukan

`chapter-17.tex` — §Studi Kasus Smart City.
