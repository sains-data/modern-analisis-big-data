# Latihan 3 — DataFrame API: Analisis Nilai Mahasiswa
**Chapter 5 · Apache Spark** | Estimasi waktu: **40 menit**

## Tujuan

- Membaca CSV dari HDFS dengan DataFrame API
- Menerapkan transformasi (`withColumn`, `groupBy`) dan action (`show`, `write`)
- Menggunakan Spark SQL melalui temporary view
- Menyimpan hasil ke Parquet di HDFS

## Prasyarat

- [ ] Latihan 1 selesai — `mahasiswa.csv` ada di `/user/lab/modul5/`
- [ ] Latihan 2 selesai (pemahaman dasar PySpark)

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input HDFS | `hdfs:///user/lab/modul5/mahasiswa.csv` |
| Output HDFS | `hdfs:///user/lab/modul5/hasil_nilai/` |
| Script | `app/analisis_nilai.py` |

## Langkah Kerja

### 1) Jalankan analisis

```bash
cd ../Konfigurasi-lab
bash scripts/run_analisis_nilai.sh
```

### 2) Verifikasi output Parquet

```bash
bash scripts/spark_exec.sh "hdfs dfs -ls /user/lab/modul5/hasil_nilai/"
bash scripts/spark_exec.sh "hdfs dfs -du -h /user/lab/modul5/hasil_nilai/"
```

## Hasil yang Dicatat

- Tabel nilai akhir per mahasiswa
- Distribusi grade (A–E)
- Hasil query SQL
- Ukuran folder output Parquet

## Refleksi Singkat

1. Berapa job yang muncul di Spark UI untuk setiap `show()` dan `write()`?
2. Mengapa `groupBy("grade")` memicu shuffle stage?

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Pemantauan Spark UI dan YARN UI**.*
