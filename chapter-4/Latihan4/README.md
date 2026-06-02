# Latihan 4 — Menjalankan MapReduce Word Count
**Chapter 4 · Ekosistem Hadoop** | Estimasi waktu: **35 menit**

## Tujuan

- Menjalankan job MapReduce contoh (`WordCount`)
- Mengamati progres eksekusi di YARN
- Membaca output hasil reduce dari HDFS

## Prasyarat

- [ ] Latihan 3 selesai
- [ ] Direktori `/user/latihan/input` siap

## Langkah Kerja

### 1) Siapkan dataset input

```bash
cd ../Konfigurasi-lab
bash scripts/prepare_wordcount_input.sh
```

File sumber: `data/dataset_wordcount.txt`

### 2) Jalankan WordCount

```bash
bash scripts/run_wordcount.sh
```

Saat job jalan, buka http://localhost:8088

### 3) Verifikasi output (opsional)

```bash
bash scripts/hadoop_exec.sh "hdfs dfs -get /user/latihan/output/part-r-00000 /tmp/hasil_wordcount.txt && cat /tmp/hasil_wordcount.txt"
```

Atau manual di `bash login.sh` dengan `hdfs dfs -cat ...`

## Hasil yang Dicatat

- Kata dengan frekuensi tertinggi
- Status aplikasi YARN (`RUNNING -> SUCCEEDED`)
- Persentase progres fase map dan reduce

## Refleksi Singkat

1. Kenapa fase reduce menunggu map selesai?
2. Apa fungsi fase `shuffle and sort` dalam hasil akhir?

---

*Latihan 4 selesai. Lanjut ke **Latihan 5 — Manajemen Data HDFS dan Re-run Job**.*
