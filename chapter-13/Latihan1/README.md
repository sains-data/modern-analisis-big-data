# Latihan 1 — Persiapan Lingkungan Monitoring
**Chapter 13 · Monitoring Infrastruktur Big Data** | Estimasi: **25 menit** | **Tahap 1**

## Tujuan

- Menjalankan stack **Prometheus + Node Exporter + Grafana**
- Memverifikasi target scrape dan alert rules ter-load

## Prasyarat

- [ ] [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Docker aktif, RAM ≥ 4 GB

## Langkah kerja

```bash
cd sesi-praktikum/chapter-13/Konfigurasi-lab
chmod +x start.sh stop.sh scripts/*.sh
bash start.sh
sleep 30
bash scripts/verify_stack.sh
```

### Verifikasi manual (sesuai buku)

1. **Prometheus** → http://localhost:9090 → **Status → Targets**  
   - `prometheus` = UP  
   - `node-exporter` = UP  

2. **Node Exporter** → http://localhost:9100/metrics (teks metrik)

3. **Grafana** → http://localhost:3000 (`admin` / `admin`)

4. **Alerts** → http://localhost:9090/alerts — empat rule: `CPUUsageTinggi`, `MemoriKritis`, `DiskHampirPenuh`, `TargetDown` (status `inactive` saat normal)

## Tabel pencatatan

| Komponen | Status | Catatan |
|---|---|---|
| Prometheus (9090) | | |
| Node Exporter target | | |
| Grafana (3000) | | |
| Alert rules dimuat | | |

## Refleksi

1. Mengapa model *pull* Prometheus lebih cocok untuk mendeteksi target down?
2. Apa peran `evaluation_interval` di `prometheus.yml`?

---

*Latihan 1 selesai. Lanjut **Latihan 2 — PromQL**.*
