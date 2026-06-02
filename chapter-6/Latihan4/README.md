# Latihan 4 — Execution Plan & Optimasi
**Chapter 6 · Spark SQL & Medallion** | Estimasi waktu: **30 menit**

## Tujuan

- Membandingkan execution plan query narrow vs wide
- Mengidentifikasi Broadcast Hash Join vs shuffle (Exchange)
- Membenchmark performa dengan dan tanpa cache

## Prasyarat

- [ ] Latihan 2 selesai — Silver layer tersedia
- [ ] Klaster masih berjalan

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input | `hdfs:///datalake/silver/transaksi/` |
| Script | `Konfigurasi-lab/app/analisis_plan.py` |
| Spark UI | http://localhost:4040 |

## Langkah Kerja

### 1) Tinjau skrip analisis plan

Buka `Konfigurasi-lab/app/analisis_plan.py` — tiga query dengan `explain(mode="formatted")` plus benchmark cache.

### 2) Jalankan (dari host)

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
bash scripts/run_analisis_plan.sh
```

Catat output di terminal; bandingkan dengan Spark UI jika job masih terlihat.

## Tabel Pencatatan — Execution Plan

| Query | Ada `Exchange`? | Ada Broadcast? | Stage | Kata kunci menarik |
|---|---|---|---|---|
| Filter + Select | | | | |
| GroupBy + Agg | | | | |
| Broadcast Join | | | | |

## Tabel Pencatatan — Benchmark Cache

| Skenario | Durasi (detik) | Catatan |
|---|---|---|
| Tanpa cache (3 query) | | |
| Dengan cache (3 query) | | |

## Refleksi Singkat

1. Kata kunci apa di `explain()` yang menandakan shuffle?
2. Mengapa broadcast join menghindari Exchange?

---

*Latihan 4 selesai. Lanjut ke **Latihan 5 — Eksplorasi Mandiri: Window & SQL**.*
