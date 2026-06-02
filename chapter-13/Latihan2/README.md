# Latihan 2 — Eksplorasi PromQL
**Chapter 13 · Monitoring Infrastruktur Big Data** | Estimasi: **30 menit** | **Tahap 2**

## Tujuan

- Menjalankan query PromQL di **Expression Browser**
- Mencatat nilai CPU, memori, disk, load, network

## Prasyarat

- [ ] Latihan 1 — stack monitoring berjalan

## Langkah kerja

1. Buka http://localhost:9090/graph  
2. Ikuti query di `Konfigurasi-lab/scripts/promql_latihan.md` **satu per satu**  
3. Catat hasil tab **Graph** dan **Table**

### Query inti (dari buku)

| # | Query | Yang dicatat |
|---|---|---|
| 1 | `{job="node-exporter"}` | Banyak series metrik |
| 2 | CPU % (idle rate) | Nilai % |
| 3 | Memory % | Nilai % |
| 4 | Disk % per filesystem | Mountpoint tertinggi |
| 5 | Uptime jam | Jam |
| 6 | `predict_linear(...) < 0` | 0 atau 1 (alert disk) |
| 7 | `node_load1/5/15` | Tiga nilai |
| 8 | Network Rx KB/s | Sesuaikan `device` jika perlu |

> Query 8 di buku memakai `device="eth0"`. Di Mac/Docker sering `en0` atau tanpa filter — gunakan versi di `promql_latihan.md`.

## Tabel observasi

| Metrik | Nilai saat ini | Catatan |
|---|---|---|
| CPU usage (%) | | |
| Memory usage (%) | | |
| Disk usage (%) | | |
| Load average 1m | | |
| Uptime (jam) | | |
| Network Rx (KB/s) | | |

## Pertanyaan refleksi (buku)

1. Mengapa pakai `rate()` pada counter CPU, bukan nilai mentah?
2. Mengapa `predict_linear(...) < 0` untuk disk penuh?
3. Load average berapa yang dianggap overload jika core = N?

---

*Latihan 2 selesai. Lanjut **Latihan 3 — Dashboard Grafana**.*
