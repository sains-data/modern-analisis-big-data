# Latihan 4 — Evaluasi Kualitas Dashboard
**Chapter 14** | Estimasi: **30 menit** | **Tahap 4**

## Tujuan

- Mengukur performa API Superset (`measure_superset_perf.sh`)
- Mengisi checklist kualitas dashboard (buku Tabel 14-checklist)
- UAT sederhana (3 skenario)

## Prasyarat

- [ ] Latihan 3 — dashboard dengan chart RFM + MoM

## Langkah kerja

### 1) Uji performa

```bash
cd sesi-praktikum/chapter-14/Konfigurasi-lab
# Ganti ID chart dari UI Superset (Charts → buka chart → URL)
bash scripts/measure_superset_perf.sh 1
```

Target buku: load time chart **< 5 detik**.

### 2) Checklist kualitas

| Aspek | Terpenuhi? | Skor 1–5 | Catatan |
|---|---|---|---|
| Data terverifikasi | | | |
| Periode & unit jelas | | | |
| Judul chart jelas | | | |
| Palet warna konsisten | | | |
| Native filter berfungsi | | | |
| Load time < 5 dtk | | | |
| **Total** | | /30 | |

### 3) UAT

| Skenario | Waktu (dtk) | Klik |
|---|---|---|
| Bulan omzet tertinggi | | |
| Kategori share terbesar | | |
| Bandingkan MoM Okt vs Nov | | |

## Refleksi

1. Skenario UAT mana yang paling sulit? Mengapa?
2. Apa perbedaan metrik teknis (load time) vs SUS/UAT?

---

*Lanjut **Latihan 5 — Refleksi Akhir (Tahap 5)**.*
