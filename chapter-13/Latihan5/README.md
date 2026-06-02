# Latihan 5 — Eksplorasi Mandiri
**Chapter 13 · Monitoring Infrastruktur Big Data** | Estimasi: **25 menit** | **Tahap 5**

## Tujuan

- Panel disk, alert tambahan, ekspor dashboard
- Menjawab pertanyaan diskusi buku

## Prasyarat

- [ ] Latihan 1–4 selesai

## Tugas A — Panel Disk Usage

Tambahkan panel **Time Series** ke dashboard:

```promql
(node_filesystem_size_bytes{fstype!="tmpfs"}
 - node_filesystem_avail_bytes{fstype!="tmpfs"})
/ node_filesystem_size_bytes{fstype!="tmpfs"} * 100
```

Legend: `{{mountpoint}}` — threshold warna jika > 85%.

## Tugas B — Alert disk & network

Lihat contoh di `prometheus/alert_rules_tugas_b.yml.example`, tambahkan ke `prometheus/alert_rules.yml`:

1. **DiskPredictedFull** — `predict_linear(...[1h], 4*3600) < 0`  
2. **NetworkTrafficTinggi** — receive > 50 MB/s  

Reload:

```bash
bash scripts/reload_prometheus.sh
```

Verifikasi di http://localhost:9090/rules

## Tugas C — Ekspor dashboard JSON

```bash
bash scripts/export_grafana_dashboard.sh BigData
# → bigdata_dashboard_backup.json
```

## Pertanyaan diskusi (buku)

1. Apakah kenaikan CPU linear dengan jumlah thread?
2. Load average > jumlah core — implikasi untuk Spark di node sama?
3. Monitoring reaktif vs proaktif — kapan `predict_linear` lebih baik dari threshold statik?
4. Mengapa `for: 5m` pada alert CPU penting?
5. Perbedaan Grafana vs Superset (data, user, refresh)?

## Penutup

```bash
bash stop.sh
```

---

*Latihan 5 selesai. Chapter 13 praktik tuntas.*
