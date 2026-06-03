# Katalog Data — Chapter 10

Dataset latihan streaming berasal dari generator sintesis Gaussian Copula (`synthetic-data/`), entitas **`catatan_aktivitas`** + **`sensor`**, diekspor ke format legacy Kafka JSON dengan alias kolom.

> **Dua sumber data:** file seed statis di `data/` (seed 42) vs **`producer_transaksi.py`** runtime (UUID acak per event). Schema sama; nilai berbeda per run producer.

## File sumber

| Path | Format | Volume | Entitas kanonik |
|------|--------|--------|-----------------|
| `data/transaksi_historis.json` | JSON legacy | **100 record** | `catatan_aktivitas` |
| `data/sample_events.json` | JSON legacy | **10 record** | subset transaksi |
| `data/sensor_iot_historis.json` | JSON legacy | **100 record** | `sensor` |
| `data/transaksi_duplikat_test.json` | JSON legacy | **50 record** (40 unik) | uji duplikat |
| `data/catatan_aktivitas_streaming.json` | JSON kanonik | 100 record | `catatan_aktivitas` |
| `data/pembacaan_sensor.json` | JSON kanonik | 100 record | `sensor` |
| `data/referensi_schema.json` | JSON schema | — | dokumentasi topic |

Salinan identik juga ada di `chapter-10/Data/` (legacy JSON saja).

## Mapping alias — topic `transaksi-stream`

| Kolom Kafka (legacy) | Kolom kanonik | Tipe |
|----------------------|---------------|------|
| `event_id` | `id_aktivitas` (8 char dari UUID) | string |
| `user_id` | `id_partisipan` (`usr-0001` = `PK-0001`) | string |
| `product` | `kelas_layanan` | string |
| `channel` | `saluran` | string |
| `amount` | `nilai_total` | double |
| `event_time` | `event_time` | ISO 8601 UTC |

## Mapping alias — topic `sensor-iot`

| Kolom Kafka (legacy) | Kolom kanonik | Tipe |
|----------------------|---------------|------|
| `event_id` | `event_id` | string |
| `sensor_id` | `sensor_id` | string |
| `location` | `lokasi` | string |
| `temperature` | `suhu` | double |
| `humidity` | `kelembapan` | double |
| `status` | `status` | normal / warning / critical |
| `event_time` | `event_time` | ISO 8601 UTC |

## Anomali terkontrol

| File | Kasus | Detail |
|------|-------|--------|
| `transaksi_historis.json` | Late / out-of-order | `event_time` tidak monoton (~48% pasangan adjacent out-of-order) — uji watermark |
| `transaksi_duplikat_test.json` | Duplikat `event_id` | **10** ID duplikat (baris 41–50 = salinan ID baris 1–10) → **40 unik** dari 50 event |

## Distribusi data (seed 42)

| Dimensi | Transaksi (100) | Sensor (100) |
|---------|-----------------|--------------|
| Pool partisipan | 50 (`usr-0001` … `usr-0050`) | — |
| Kelas / lokasi | 6 produk, 4 saluran | 5 lokasi, 20 sensor_id |
| Partisipan aktif | ~32 user_id unik | — |
| Rentang nilai | ~Rp 97 ribu – ~Rp 98 juta | suhu 20–45 °C, kelembapan 30–90% |

## Topic Kafka

| Topic | Partisi | File seed | Penggunaan |
|-------|---------|-----------|------------|
| `transaksi-stream` | 3 | `transaksi_historis.json` | Producer + Spark streaming |
| `sensor-iot` | 2 | `sensor_iot_historis.json` | Latihan 5 |
| `penjualan-agregat` | 1 | — (output Spark) | Agregat window |

## Regenerasi data

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch10_streaming
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
