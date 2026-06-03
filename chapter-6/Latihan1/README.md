# Latihan 1 — Persiapan Dataset Bronze
**Chapter 6 · Spark SQL & Medallion** | Estimasi waktu: **25 menit**

## Tujuan

- Membuat struktur direktori medallion di HDFS
- Menyiapkan dataset catatan aktivitas & partisipan (dengan anomali terkontrol)
- Mengunggah data mentah ke layer Bronze tanpa modifikasi

## Prasyarat

- [ ] Setup lab — [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Klaster berjalan (`bash start.sh` dari folder `Konfigurasi-lab`)
- [ ] File data tersedia — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Referensi data

| File | Volume | Entitas kanonik |
|------|--------|-----------------|
| `data/transaksi.csv` | **16 baris** | `catatan_aktivitas` |
| `data/pelanggan.csv` | **7 baris** | `entitas_partisipan` |

Partisipan C001–C007 selaras dengan PK-0001–PK-0007 (Bab 3 & 5).

## Referensi Lingkungan Lab

| Path HDFS | Isi |
|---|---|
| `/datalake/bronze/transaksi/` | `transaksi.csv` |
| `/datalake/bronze/pelanggan/` | `pelanggan.csv` |
| `/datalake/silver/transaksi/` | (kosong, diisi Latihan 2) |
| `/datalake/gold/per_kategori/` | (kosong, diisi Latihan 3) |
| `/datalake/gold/per_segmen/` | (kosong, diisi Latihan 3) |

## Langkah Kerja

### 1) Jalankan klaster (dari host)

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
bash start.sh
bash scripts/verify_cluster.sh
```

### 2) Setup medallion & upload Bronze

```bash
bash scripts/setup_datalake_bronze.sh
```

### 3) Verifikasi (opsional)

```bash
bash scripts/verify_datalake.sh
# atau di kontainer:
bash login.sh
hdfs dfs -cat /datalake/bronze/transaksi/transaksi.csv | wc -l
exit
```

Harapan: **17 baris** output `wc -l` (16 data + 1 header) — atau 16 baris data.

### 4) Inspeksi anomali

Buka `Konfigurasi-lab/data/transaksi.csv`:

| ID | Anomali |
|----|---------|
| TRX001 | Duplikat (baris 1 & 16 identik) |
| TRX011 | `id_pelanggan` kosong |
| TRX012 | `jumlah` = −150.000 |
| TRX013 | `kuantitas` = 0 |
| TRX014 | `kota` = `palembang` (lowercase) |

## Refleksi Singkat

1. Mengapa Bronze tidak boleh dimodifikasi setelah di-upload?
2. Berapa baris yang Anda prediksi akan lolos ke Silver? (petunjuk: [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md))

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — Pipeline Bronze ke Silver**.*
