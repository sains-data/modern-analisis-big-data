# Latihan 3 — Operasi Dasar HDFS
**Chapter 4 · Ekosistem Hadoop** | Estimasi waktu: **30 menit**

## Tujuan

- Melakukan operasi dasar file system di HDFS
- Memeriksa blok, lokasi data, dan kapasitas klaster

## Prasyarat

- [ ] Latihan 1–2 selesai
- [ ] Klaster berjalan (`bash start.sh`)

## Langkah Kerja

Dari host (`Konfigurasi-lab/`):

```bash
cd ../Konfigurasi-lab
bash scripts/setup_hdfs_latihan.sh
```

Skrip memakai `data/latihan.txt` dan menjalankan `mkdir`, `put`, `cat`, `fsck`, `dfsadmin -report`.

Manual di dalam kontainer (`bash login.sh`) — sama seperti di atas dengan `hdfs dfs ...`.

## Hasil yang Dicatat

- Jumlah blok file `latihan.txt`
- Lokasi blok pada DataNode
- Jumlah `live datanodes`
- Ringkasan `Configured Capacity`, `DFS Used`, `DFS Remaining`

## Refleksi Singkat

1. Kenapa file kecil tetap menempati 1 blok HDFS?
2. Jelaskan prinsip `write-once, read-many` pada HDFS.

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Menjalankan MapReduce Word Count**.*
