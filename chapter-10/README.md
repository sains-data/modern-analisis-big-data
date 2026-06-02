# Chapter 10 — Analitik Aliran Data

Praktik chapter ini membangun pipeline **streaming end-to-end**: producer Python → **Apache Kafka** (KRaft) → **Spark Structured Streaming** (windowing, checkpoint).

Sumber materi: bagian **Sesi Praktik: Pipeline Streaming Kafka–Spark End-to-End** di `chapter-10.tex`.

## Komponen

| Komponen | Versi |
|---|---|
| Apache Kafka | 3.7.x (KRaft, Docker) |
| Spark Structured Streaming | 3.5.5 |
| Python | 3.10 atau 3.11 (wajib untuk PySpark) |
| Durasi estimasi | 2,5–3 jam (5 latihan) |

## Struktur folder

```
chapter-10/
├── Konfigurasi-lab/     ← docker-compose Kafka, skrip producer/Spark
├── Data/                ← JSON seed & referensi schema
├── Latihan1/ … Latihan5/
└── README.md
```

## Alur cepat

```bash
cd sesi-praktikum/chapter-10/Konfigurasi-lab
bash start.sh
bash scripts/setup_venv.sh && source .venv/bin/activate
# Latihan 1 → 5 (semua dari folder Konfigurasi-lab/)
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Port & layanan

| Port | Layanan |
|---|---|
| 9092 | Kafka broker (`localhost:9092`) |
| 8080 | Kafka UI |
| 4040 | Spark UI (saat `spark-submit` berjalan) |

## Daftar latihan

| Latihan | Topik (sesuai bab) | Estimasi |
|---|---|---|
| [Latihan 1](Latihan1/README.md) | Setup Kafka, topic, uji producer/consumer CLI | 10 menit |
| [Latihan 2](Latihan2/README.md) | Producer Python — event transaksi ke Kafka | 20 menit |
| [Latihan 3](Latihan3/README.md) | Spark Structured Streaming + windowing | 35 menit |
| [Latihan 4](Latihan4/README.md) | Fault tolerance — checkpoint & recovery | 15 menit |
| [Latihan 5](Latihan5/README.md) | Tumbling vs sliding window, delivery semantics | 10 menit |

## Topic Kafka latihan

| Topic | Partisi | Penggunaan |
|---|---|---|
| `transaksi-stream` | 3 | Producer + Spark streaming utama |
| `sensor-iot` | 2 | Eksplorasi (Latihan 5) |
| `penjualan-agregat` | 1 | Agregat output (opsional) |

> Nama kontainer `modul8-kafka-broker` berasal dari Docker Compose lab; dipakai untuk Chapter 10.

## Catatan Python

- Didukung: **Python 3.10 / 3.11**
- Tidak disarankan: Python 3.12 (`pyspark==3.5.5`)
