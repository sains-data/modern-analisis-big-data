# Latihan 2 — PySpark Pertama: Aproksimasi Pi (Monte Carlo)
**Chapter 5 · Apache Spark** | Estimasi waktu: **35 menit**

## Tujuan

- Membuat `SparkSession` dengan master YARN
- Menjalankan komputasi terdistribusi menggunakan RDD API
- Memahami peran `--master yarn` pada `spark-submit`

## Prasyarat

- [ ] Latihan 1 selesai
- [ ] Klaster Hadoop-Spark masih berjalan

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Script | `app/hitung_pi.py` → `/opt/spark-jobs/hitung_pi.py` |
| Master | `yarn` |
| Deploy mode | `client` |
| Spark UI | http://localhost:4040 |
| YARN UI | http://localhost:8088 |

## Langkah Kerja

### 1) Skrip

File: `Konfigurasi-lab/app/hitung_pi.py` (Monte Carlo, `SLICES` via env).

### 2) Submit ke YARN (dari host)

```bash
cd ../Konfigurasi-lab
bash scripts/run_hitung_pi.sh
```

Saat job berjalan, buka:
- Spark UI: http://localhost:4040
- YARN UI: http://localhost:8088

## Hasil yang Dicatat

- Versi Spark dan master yang terdeteksi
- Nilai aproksimasi Pi
- Selisih terhadap nilai referensi
- Jumlah job/stage yang muncul di Spark UI

## Refleksi Singkat

1. Mengapa `parallelize()` cocok untuk uji performa klaster?
2. Apa perbedaan `--master yarn` vs `--master local[4]`?

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — DataFrame API: Analisis Nilai Mahasiswa**.*
