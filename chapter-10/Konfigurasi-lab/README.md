# Konfigurasi Lab Chapter 10

Konfigurasi ini menyelesaikan mismatch Python dengan memaksa environment ke Python **3.10/3.11**, karena `pyspark==3.5.5` tidak aman dipakai di Python 3.12.

## Referensi Lingkungan

| Item | Nilai |
|---|---|
| Kafka broker | `modul8-kafka-broker` (port `9092`) |
| Kafka UI | http://localhost:8080 |
| Spark UI | http://localhost:4040 (saat job Spark berjalan) |
| Python venv | `.venv` (Python 3.10 atau 3.11) |
| Topic latihan | `transaksi-stream` (3 partisi), `sensor-iot` (2), `penjualan-agregat` (1) |

## 1) Jalankan stack Kafka

```bash
cd Konfigurasi-lab
bash start.sh
```

UI:
- Kafka UI: `http://localhost:8080`

## 2) Siapkan Python environment

```bash
bash scripts/setup_venv.sh
source .venv/bin/activate
```

Script `setup_venv.sh` akan gagal otomatis jika Python bukan `3.10` atau `3.11`.

## 3) Jalankan producer dan Spark

Terminal 1:
```bash
source .venv/bin/activate
python scripts/producer_transaksi.py
```

Terminal 2:
```bash
source .venv/bin/activate
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  --master local[2] \
  spark/streaming_agregasi.py
```

## 4) Seed data historis (opsional)

```bash
source .venv/bin/activate
python scripts/seed_kafka.py --file data/transaksi_historis.json
python scripts/seed_kafka.py --topic sensor-iot --file data/sensor_iot_historis.json
```

## 5) Script latihan tambahan

| File | Digunakan di |
|---|---|
| `spark/window_comparison.py` | Latihan 5 — tumbling vs sliding window |
| `scripts/consumer_semantics.py` | Latihan 5 — analisis delivery semantics |

## 6) Hentikan stack

```bash
bash stop.sh
```
