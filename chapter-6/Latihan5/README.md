# Latihan 5 — Eksplorasi Mandiri: Window Function & SQL
**Chapter 6 · Spark SQL & Medallion** | Estimasi waktu: **25 menit**

## Tujuan

- Menerapkan window function (`rank`, running sum) pada data Silver
- Menjalankan query Spark SQL langsung pada Silver layer
- Menjawab pertanyaan diskusi arsitektur medallion

## Prasyarat

- [ ] Latihan 1–4 selesai
- [ ] Pipeline Bronze → Silver → Gold sudah berjalan

## Langkah Kerja

### Bagian A — Window function

Skrip: `Konfigurasi-lab/app/window_function.py`

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
bash scripts/run_window_function.sh
```

### Bagian B — Spark SQL pada Silver

Skrip: `Konfigurasi-lab/app/sql_silver.py`

```bash
bash scripts/run_sql_silver.sh
```

## Pertanyaan Diskusi

1. Apakah strategi membuang baris invalid (TRX011, TRX012) sudah tepat? Alternatif apa yang bisa diusulkan?
2. Apa yang terjadi jika DataFrame pelanggan 500 MB tetap di-broadcast?
3. Kata kunci apa di `explain()` yang membedakan query wide vs narrow?
4. Mengapa data Bronze tidak boleh dimodifikasi setelah ditulis?

## Penutup

Verifikasi pipeline end-to-end:

```bash
bash scripts/verify_datalake.sh
bash stop.sh
```

---

*Latihan 5 selesai. Chapter 6 praktik tuntas.*
