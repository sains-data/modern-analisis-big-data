# Latihan 4 — Pemantauan Spark UI dan YARN UI
**Chapter 5 · Apache Spark** | Estimasi waktu: **20 menit**

## Tujuan

- Membaca metrik eksekusi job Spark dari Spark UI
- Memantau alokasi resource aplikasi di YARN UI
- Membandingkan ukuran data CSV vs Parquet di HDFS

## Prasyarat

- [ ] Latihan 2–3 selesai (minimal satu job Spark sudah dijalankan)
- [ ] Klaster masih berjalan

## Referensi Lingkungan Lab

| Antarmuka | URL | Fokus observasi |
|---|---|---|
| Spark UI | http://localhost:4040 | Jobs, Stages, Executors, SQL plan |
| YARN RM | http://localhost:8088 | Aplikasi, container, log |
| NameNode UI | http://localhost:9870 | Kapasitas HDFS, browse file |

## Langkah Kerja

### 1) Amati Spark UI

Buka http://localhost:4040, lalu catat dari tab:
- **Jobs** — jumlah job selesai
- **Stages** — total stage dan stage dengan shuffle
- **Executors** — memori terpakai
- **SQL** — query plan (jika ada)

### 2) Amati YARN UI

Buka http://localhost:8088, lalu catat:
- Status aplikasi Spark (`RUNNING` / `FINISHED`)
- Jumlah container yang dialokasikan
- Log aplikasi (jika perlu troubleshooting)

### 3) Bandingkan ukuran file HDFS

Input CSV berisi **10 baris** skor kompetensi; output Parquet berisi 10 baris + kolom turunan (`nilai_akhir`, `grade`).

```bash
cd ../Konfigurasi-lab
bash scripts/compare_hdfs_sizes.sh
```

## Tabel Pencatatan

| Informasi | Nilai |
|---|---|
| Jumlah Job (Spark UI) | |
| Jumlah Stage total | |
| Stage yang melibatkan Shuffle | |
| Memori Executor | |
| Status aplikasi di YARN | |
| Ukuran file CSV di HDFS | |
| Ukuran folder Parquet di HDFS | |

## Refleksi Singkat

1. Mengapa Parquet biasanya lebih kecil/efisien dibanding CSV untuk analitik?
2. Apa indikator di YARN UI bahwa resource klaster sudah penuh?

---

*Latihan 4 selesai. Lanjut ke **Latihan 5 — Eksplorasi Mandiri: Partisi dan Caching**.*
