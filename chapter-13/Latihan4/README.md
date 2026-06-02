# Latihan 4 — Alert & Observasi Saat Beban
**Chapter 13 · Monitoring Infrastruktur Big Data** | Estimasi: **30 menit** | **Tahap 4**

## Tujuan

- Memeriksa **alert rules** di Prometheus
- Menghasilkan beban CPU dan mengamati metrik
- Mengorelasikan perubahan di Grafana

## Prasyarat

- [ ] Latihan 3 — dashboard tersimpan

## Langkah kerja

### 4.1 Periksa alerts

http://localhost:9090/alerts — empat rule, status `inactive` (kondisi normal).

### 4.2 Beban CPU (terminal A)

```bash
cd sesi-praktikum/chapter-13/Konfigurasi-lab
bash scripts/cpu_stress.sh 2 60
```

(2 thread, 60 detik — sesuai buku)

### 4.3 Polling CPU (terminal B)

```bash
bash scripts/poll_cpu.sh
```

### 4.4 Grafana

- Buka dashboard `BigData Infrastructure Monitoring`
- Time range: **Last 5 minutes**, refresh **5s**
- Amati: warna gauge CPU, mode `user`/`system`, load average

## Tabel pengamatan

| Pengamatan | Sebelum | Selama | Sesudah |
|---|---|---|---|
| CPU usage (%) | | | |
| Load average 1m | | | |
| Memory usage (%) | | | |
| Waktu pulih (detik) | — | — | |

## Refleksi

1. Mode CPU mana yang naik paling jelas saat beban?
2. Apakah load average ~2 saat 2 thread stress?

---

*Latihan 4 selesai. Lanjut **Latihan 5 — Eksplorasi Mandiri**.*
