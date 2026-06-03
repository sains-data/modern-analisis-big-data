# Latihan 3 — Operasi Dasar HDFS
**Chapter 4 · Ekosistem Hadoop** | Estimasi waktu: **30 menit**

## Tujuan

- Melakukan operasi dasar file system di HDFS
- Memeriksa blok, lokasi data, dan kapasitas klaster

## Prasyarat

- [ ] Latihan 1–2 selesai
- [ ] Klaster berjalan (`bash start.sh`)
- [ ] File `data/latihan.txt` tersedia (7 kalimat — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md))

## Referensi data

File `latihan.txt` memuat narasi tentang:
- Platform **partisipan** dan **saluran** interaksi
- **HDFS**, blok 128MB, NameNode, DataNode
- Pipeline **bronze → silver → gold**
- **Unit geografis** Jakarta, Surabaya, Bandung

Kosakata ini selaras dengan dataset sintesis Bab 3+.

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
- Satu kalimat dari isi file yang berhasil di-`cat`

## Refleksi Singkat

1. Kenapa file kecil tetap menempati 1 blok HDFS?
2. Jelaskan prinsip `write-once, read-many` pada HDFS.
3. Bagaimana file teks ini terhubung dengan pipeline medallion di Bab 3?

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Menjalankan MapReduce Word Count**.*
