# Keterangan File Data — Chapter 10

File data latihan tersedia di dua lokasi (isi sama):
- `Data/` — referensi dan dokumentasi
- `Konfigurasi-lab/data/` — dipakai saat menjalankan lab

## Daftar File

| File | Jumlah Record | Digunakan Di | Keterangan |
|---|---|---|---|
| `sample_events.json` | 10 | Latihan 1, 2 | Referensi schema dan contoh format event transaksi |
| `transaksi_historis.json` | 500 | Latihan 2, 3 | Data seed untuk topic `transaksi-stream` sebelum latihan dimulai |
| `sensor_iot_historis.json` | 300 | Latihan 5 (eksplorasi) | Data seed untuk topic `sensor-iot` |
| `transaksi_duplikat_test.json` | 50 (40 unik) | Latihan 5 Bagian B | 50 event dengan 10 `event_id` duplikat untuk uji delivery semantics |
| `referensi_schema.json` | — | Semua latihan | Dokumentasi lengkap schema semua topic Kafka |
| `seed_kafka.py` | — | Setup awal | Script Python untuk mengirim data historis ke Kafka |

## Cara Menggunakan

Jalankan dari folder **`Konfigurasi-lab/`** dengan venv aktif:

```bash
cd Konfigurasi-lab
source .venv/bin/activate
```

### Seed topic `transaksi-stream` (untuk Latihan 2 & 3):

```bash
python scripts/seed_kafka.py --file data/transaksi_historis.json
```

### Seed topic `sensor-iot` (untuk Latihan 5):

```bash
python scripts/seed_kafka.py \
  --topic sensor-iot \
  --file data/sensor_iot_historis.json
```

### Seed topic untuk uji delivery semantics (Latihan 5 Bagian B):

```bash
python scripts/seed_kafka.py \
  --topic transaksi-stream \
  --file data/transaksi_duplikat_test.json \
  --delay 0.0
```

## Catatan Penting

- Semua `event_time` menggunakan format **ISO 8601 UTC** (`+00:00`)
- `transaksi_historis.json` mengandung sebagian event out-of-order untuk mensimulasikan late data
- `transaksi_duplikat_test.json` memiliki **10 dari 50 event_id yang duplikat**
- Pastikan Kafka sudah berjalan (`bash start.sh`) sebelum menjalankan seed
