# Latihan 1 — Persiapan Lingkungan & Data Bronze
**Chapter 8 · Struktur & Penyimpanan Big Data** | Estimasi waktu: **25 menit**

## Tujuan

- Memverifikasi Hadoop, YARN, Hive Metastore, dan HBase aktif
- Menyiapkan **500 transaksi** sintetis dan **50 pelanggan** (generator Gaussian Copula)
- Mengunggah data mentah ke HDFS (layer Bronze)

## Prasyarat

- [ ] Setup lab — [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] RAM minimal 10 GB, Docker aktif
- [ ] Enam tarball di `vendor/bigdata-spark/` (lihat Konfigurasi-lab)
- [ ] File data tersedia — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Referensi data

| File | Volume | Entitas kanonik |
|------|--------|-----------------|
| `data/transaksi.csv` | **500 baris** | `catatan_aktivitas` |
| `data/pelanggan.csv` | **50 baris** | `entitas_partisipan` |

ID legacy: `TRX-00001` … `TRX-00500`, `PLG-0001` … `PLG-0050` (≡ `PK-0001` … `PK-0050`).

## Referensi Lingkungan Lab

| Path HDFS | Isi |
|---|---|
| `/datalake/bronze/transaksi/` | `data.csv` (500 baris) |
| `/datalake/bronze/pelanggan/` | `data.csv` (50 baris) |

Data sumber: `Konfigurasi-lab/data/transaksi.csv`, `pelanggan.csv`.

## Langkah Kerja

### 1) Build & jalankan klaster (dari host)

```bash
cd sesi-praktikum/chapter-8/Konfigurasi-lab
bash build.sh
bash start.sh
bash scripts/verify_cluster.sh
```

Tunggu bootstrap selesai jika ada proses `[MISSING]`:

```bash
bash scripts/spark_exec.sh "tail -30 /tmp/bootstrap.log"
```

### 2) Setup layanan & upload Bronze

```bash
bash scripts/setup_datalake_bronze.sh
```

Perintah di atas memulai HBase Thrift, Hive metastore (jika perlu), membuat folder `/datalake/`, dan mengunggah CSV sebagai `data.csv`.

### 3) Verifikasi manual (opsional)

```bash
bash login.sh
jps
hdfs dfs -ls /datalake/bronze/
exit
```

Atau dari host: `bash scripts/verify_datalake.sh`

### 4) Regenerasi data (opsional)

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch08_storage
bash scripts/sync_to_chapters.sh
```

Seed default: `42`. Skrip lokal `app/buat_data_bronze.py` hanya fallback lama — gunakan generator di atas agar selaras modul lain.

## Hasil yang Dicatat

- Daftar proses dari `jps` (NameNode, HMaster, HRegionServer, …)
- Jumlah baris (**500** transaksi, **50** pelanggan)
- Konfirmasi file di HDFS

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — Hive & Spark SQL**.*
