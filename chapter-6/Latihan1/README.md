# Latihan 1 — Persiapan Dataset Bronze
**Chapter 6 · Spark SQL & Medallion** | Estimasi waktu: **25 menit**

## Tujuan

- Membuat struktur direktori medallion di HDFS
- Menyiapkan dataset transaksi dan pelanggan (dengan anomali sengaja)
- Mengunggah data mentah ke layer Bronze tanpa modifikasi

## Prasyarat

- [ ] Setup lab — [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Klaster berjalan (`bash start.sh` dari folder `Konfigurasi-lab`)

## Referensi Lingkungan Lab

| Path HDFS | Isi |
|---|---|
| `/datalake/bronze/transaksi/` | `transaksi.csv` |
| `/datalake/bronze/pelanggan/` | `pelanggan.csv` |
| `/datalake/silver/transaksi/` | (kosong, diisi Latihan 2) |
| `/datalake/gold/per_kategori/` | (kosong, diisi Latihan 3) |
| `/datalake/gold/per_segmen/` | (kosong, diisi Latihan 3) |

Data sumber ada di repo: `Konfigurasi-lab/data/transaksi.csv` dan `pelanggan.csv`.

## Langkah Kerja

### 1) Jalankan klaster (dari host)

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
bash start.sh
bash scripts/verify_cluster.sh
```

### 2) Setup medallion & upload Bronze

Satu perintah membuat folder HDFS dan mengunggah CSV:

```bash
bash scripts/setup_datalake_bronze.sh
```

### 3) Verifikasi (opsional, di dalam kontainer)

```bash
bash login.sh
hdfs dfs -ls /datalake/
hdfs dfs -cat /datalake/bronze/transaksi/transaksi.csv | head -5
exit
```

Atau dari host:

```bash
bash scripts/verify_datalake.sh
```

### 4) Inspeksi data lokal (opsional)

Buka `Konfigurasi-lab/data/transaksi.csv` — 15 baris dengan anomali terencana.

## Anomali yang Harus Dikenali

| Masalah | Contoh |
|---|---|
| Duplikasi | TRX001 (2×) |
| ID pelanggan kosong | TRX011 |
| Nilai negatif | TRX011 (`jumlah` = -150000) |
| Kuantitas nol | TRX012 |
| Spasi / inkonsistensi kota | `" Sepatu "`, `JAKARTA`, `yogyakarta` |

## Refleksi Singkat

1. Mengapa Bronze tidak boleh dimodifikasi setelah di-upload?
2. Berapa jenis anomali yang Anda identifikasi sebelum pipeline Silver?

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — Pipeline Bronze ke Silver**.*
