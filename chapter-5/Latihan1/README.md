# Latihan 1 — Setup Klaster dan Persiapan Data HDFS
**Chapter 5 · Apache Spark** | Estimasi waktu: **25 menit**

## Tujuan

- Menjalankan klaster Hadoop-Spark berbasis Docker
- Memverifikasi HDFS dan YARN aktif
- Menyiapkan dataset `mahasiswa.csv` di HDFS

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Tarball Hadoop & Spark ada di `vendor/bigdata-spark/` (lihat Konfigurasi-lab)

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Folder kerja | `Konfigurasi-lab/` |
| Container | `bigdata-spark` |
| Path HDFS kerja | `/user/lab/modul5/` (default di `.env`) |
| Spark UI | http://localhost:4040 |

## Langkah Kerja

### 1) Jalankan klaster

```bash
cd ../Konfigurasi-lab
cp .env.example .env    # pertama kali
bash build.sh
bash start.sh
bash scripts/verify_cluster.sh
```

### 2) Upload data mahasiswa ke HDFS

```bash
bash scripts/setup_hdfs_mahasiswa.sh
```

Opsional — shell di dalam kontainer:

```bash
bash login.sh
cat /tmp/bootstrap.log
jps
hdfs dfs -ls /user/lab/modul5/
```

## Hasil yang Dicatat

- Status daemon dari `jps`
- Ringkasan `hdfs dfsadmin -report`
- Konfirmasi file `mahasiswa.csv` ada di HDFS

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — PySpark Pertama: Aproksimasi Pi**.*
