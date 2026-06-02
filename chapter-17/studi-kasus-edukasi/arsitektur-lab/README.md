# Arsitektur Lab — Studi Kasus Edukasi

Lingkungan **batch-dominan** (ritme semester) + streaming LMS/absensi; integrasi 8+ sistem institusional simulasi.

## Isi yang direncanakan (Lampiran)

```
arsitektur-lab/
├── docker-compose.yml
├── kafka/              # lms.events, absensi.sesi
├── airflow/dags/       # mingguan + akhir semester
├── minio/              # lakehouse Iceberg
└── superset/           # dashboard PA + akreditasi
```

## Dokumentasi

→ **[PANDUAN-ARSITEKTUR-LAB.md](arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md)**

## Prasyarat

- Bab 9–11 (Kafka, Spark, ML)  
- Bab 12 (Superset)  
- Pemahaman GDPR/PDP untuk data mahasiswa  

## Rujukan

`chapter-17.tex` — §Studi Kasus Edukasi.
