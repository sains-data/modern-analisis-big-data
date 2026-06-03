# Latihan 1 — Setup Klaster dan Persiapan Data HDFS
**Chapter 5 · Apache Spark** | Estimasi waktu: **25 menit**

## Tujuan

- Menjalankan klaster Hadoop-Spark berbasis Docker
- Memverifikasi HDFS dan YARN aktif
- Menyiapkan dataset skor kompetensi (`mahasiswa.csv`) di HDFS

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Tarball Hadoop & Spark ada di `vendor/bigdata-spark/` (lihat Konfigurasi-lab)
- [ ] File `data/mahasiswa.csv` tersedia (**10 baris**) — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Referensi data

| Item | Nilai |
|------|-------|
| File lokal | `Konfigurasi-lab/data/mahasiswa.csv` |
| Volume | 10 partisipan |
| Kolom | `nim`, `nama`, `nilai_uts`, `nilai_uas`, `nilai_tugas` |
| Sumber | Generator sintesis Copula — entitas `skor_kompetensi` |
| Entitas kanonik | `data/skor_kompetensi.csv` (`id_partisipan`, `skor_modul_a/b/c`) |

Nama partisipan (Andi Saputra, Budi Santoso, …) selaras dengan Bab 3.

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

### 2) Upload data ke HDFS

```bash
bash scripts/setup_hdfs_mahasiswa.sh
```

Skrip mengunggah `mahasiswa.csv` ke `/user/lab/modul5/mahasiswa.csv`.

Opsional — shell di dalam kontainer:

```bash
bash login.sh
cat /tmp/bootstrap.log
jps
hdfs dfs -ls /user/lab/modul5/
hdfs dfs -cat /user/lab/modul5/mahasiswa.csv
```

## Hasil yang Dicatat

- Status daemon dari `jps`
- Ringkasan `hdfs dfsadmin -report`
- Konfirmasi **10 baris** data di HDFS (preview `head -5`)
- Contoh satu baris: `nim`, `nama`, tiga nilai skor

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — PySpark Pertama: Aproksimasi Pi**.*
