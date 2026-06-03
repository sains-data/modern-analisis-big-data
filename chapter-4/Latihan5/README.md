# Latihan 5 — Manajemen Data HDFS dan Re-run Job
**Chapter 4 · Ekosistem Hadoop** | Estimasi waktu: **20 menit**

## Tujuan

- Melakukan operasi manajemen data lanjutan di HDFS
- Membersihkan output agar job MapReduce dapat dijalankan ulang

## Prasyarat

- [ ] Latihan 1–4 selesai
- [ ] Direktori output WordCount sudah terbentuk

## Langkah Kerja

```bash
cd ../Konfigurasi-lab
bash scripts/hdfs_management.sh
```

## Validasi — re-run WordCount

Setelah manajemen HDFS, jalankan ulang WordCount. Output baru harus tetap menunjukkan frekuensi dominan **`partisipan`** (6) dan **`aktivitas`** (6).

```bash
bash scripts/hdfs_management.sh --rerun-wordcount
```

## Refleksi Singkat

1. Kenapa direktori output harus belum ada saat run MapReduce?
2. Jelaskan perubahan `DFS Used` sebelum dan sesudah hapus output.

## Penutup

```bash
bash stop.sh
```

---

*Latihan 5 selesai. Chapter 4 praktik tuntas.*
