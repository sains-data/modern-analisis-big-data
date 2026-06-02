# Latihan 2 — Eksplorasi Web UI Hadoop
**Chapter 4 · Ekosistem Hadoop** | Estimasi waktu: **20 menit**

## Tujuan

- Memahami informasi operasional dari NameNode UI dan ResourceManager UI
- Mencatat metrik dasar klaster

## Prasyarat

- [ ] Latihan 1 selesai
- [ ] Klaster Hadoop masih berjalan

## Langkah Kerja

1. Buka:
   - `http://localhost:9870`
   - `http://localhost:8088`
2. Amati:
   - kapasitas HDFS
   - jumlah DataNode aktif
   - jumlah NodeManager aktif
   - metrik memori/vCore YARN

## Tabel Pencatatan

| Informasi | Nilai |
|---|---|
| Versi Hadoop | |
| Configured Capacity HDFS | |
| DFS Used | |
| DFS Remaining | |
| Jumlah DataNode Aktif | |
| Total Memori Klaster (YARN) | |
| Jumlah NodeManager Aktif | |
| Jumlah vCore Tersedia | |

## Refleksi Singkat

1. Mengapa `Configured Capacity` bisa lebih kecil dari kapasitas disk fisik?
2. Apa manfaat tab `Applications` pada ResourceManager UI?

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Operasi Dasar HDFS**.*
