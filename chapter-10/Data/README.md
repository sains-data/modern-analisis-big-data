# Keterangan File Data — Chapter 10

File data latihan tersedia di dua lokasi (isi legacy JSON sama):
- `Data/` — salinan referensi
- `Konfigurasi-lab/data/` — dipakai saat menjalankan lab (+ file kanonik)

Dokumentasi lengkap mapping, anomali, dan volume: **[KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)**.

## Daftar File

| File | Jumlah Record | Digunakan Di | Keterangan |
|---|---|---|---|
| `sample_events.json` | **10** | Latihan 1, 2 | Contoh format event `transaksi-stream` |
| `transaksi_historis.json` | **100** | Latihan 2, 3 | Seed topic `transaksi-stream` (out-of-order) |
| `sensor_iot_historis.json` | **100** | Latihan 5 | Seed topic `sensor-iot` |
| `transaksi_duplikat_test.json` | **50** (**40 unik**) | Latihan 5 Bagian B | 10 `event_id` duplikat |
| `referensi_schema.json` | — | Semua latihan | Schema topic Kafka |
| `seed_kafka.py` | — | Setup awal | Salinan di `Konfigurasi-lab/scripts/` |

File kanonik (hanya di `Konfigurasi-lab/data/`):
- `catatan_aktivitas_streaming.json` — 100 record
- `pembacaan_sensor.json` — 100 record

## Cara Menggunakan

Jalankan dari folder **`Konfigurasi-lab/`** dengan venv aktif:

```bash
cd Konfigurasi-lab
source .venv/bin/activate
```

### Seed topic `transaksi-stream` (Latihan 2 & 3):

```bash
python scripts/seed_kafka.py --file data/transaksi_historis.json
```

### Seed topic `sensor-iot` (Latihan 5):

```bash
python scripts/seed_kafka.py \
  --topic sensor-iot \
  --file data/sensor_iot_historis.json
```

### Seed uji delivery semantics (Latihan 5 Bagian B):

```bash
python scripts/seed_kafka.py \
  --topic transaksi-stream \
  --file data/transaksi_duplikat_test.json \
  --delay 0.0
```

## Regenerasi data referensi

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch10_streaming
bash scripts/sync_to_chapters.sh
```

## Catatan Penting

- Semua `event_time` menggunakan format **ISO 8601 UTC** (`+00:00`)
- `transaksi_historis.json` mengandung event **out-of-order** untuk uji watermark Spark
- `transaksi_duplikat_test.json`: baris 41–50 memakai ulang `event_id` baris 1–10
- Pastikan Kafka sudah berjalan (`bash start.sh`) sebelum menjalankan seed
