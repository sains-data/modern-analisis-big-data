# Latihan 3 — DataFrame API: Analisis Skor Kompetensi
**Chapter 5 · Apache Spark** | Estimasi waktu: **40 menit**

## Tujuan

- Membaca CSV skor kompetensi dari HDFS dengan DataFrame API
- Menerapkan transformasi (`withColumn`, `groupBy`) dan action (`show`, `write`)
- Menggunakan Spark SQL melalui temporary view
- Menyimpan hasil ke Parquet di HDFS

## Prasyarat

- [ ] Latihan 1 selesai — `mahasiswa.csv` ada di `/user/lab/modul5/` (**10 baris**)
- [ ] Latihan 2 selesai (pemahaman dasar PySpark)

## Referensi data

File `mahasiswa.csv` memuat skor tiga modul per partisipan (alias legacy dari `skor_kompetensi`):

| Kolom | Modul |
|-------|-------|
| `nilai_uts` | Modul A (30%) |
| `nilai_uas` | Modul B (40%) |
| `nilai_tugas` | Modul C (30%) |

Formula: `nilai_akhir = uts×0.30 + uas×0.40 + tugas×0.30`

**Distribusi grade harapan** (verifikasi output):

| Grade | Jumlah |
|-------|--------|
| A | 1 |
| B | 2 |
| C | 3 |
| D | 3 |
| E | 1 |

Detail schema: [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

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

- Tabel nilai akhir per partisipan (10 baris)
- Distribusi grade — bandingkan dengan tabel harapan di atas
- Partisipan grade A: **Ahmad Rizky** (`2021004`, nilai akhir ≈ 85,3)
- Hasil query SQL `GROUP BY grade`
- Ukuran folder output Parquet vs CSV (`compare_hdfs_sizes.sh`)

## Refleksi Singkat

1. Berapa job yang muncul di Spark UI untuk setiap `show()` dan `write()`?
2. Mengapa `groupBy("grade")` memicu shuffle stage?
3. Bagaimana korelasi antar skor modul (Copula Blok C) tercermin di nilai akhir?

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Pemantauan Spark UI dan YARN UI**.*
