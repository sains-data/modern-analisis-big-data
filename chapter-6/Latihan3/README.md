# Latihan 3 — Pipeline Silver ke Gold (Join & Agregasi)
**Chapter 6 · Spark SQL & Medallion** | Estimasi waktu: **35 menit**

## Tujuan

- Join transaksi Silver dengan data pelanggan Bronze
- Menerapkan broadcast join dan anti join
- Menulis agregat bisnis ke layer Gold (per kategori & per segmen)

## Prasyarat

- [ ] Latihan 1–2 selesai
- [ ] Data Silver tersedia di `/datalake/silver/transaksi/`

## Referensi data

- Silver: **12 baris** transaksi valid (dari 16 Bronze)
- Pelanggan Bronze: **7 partisipan** (C001–C007, broadcast join)
- Tidak ada transaksi orphan setelah validasi Silver (TRX011 sudah ditolak di Latihan 2)

## Referensi Lingkungan Lab

| Path | Layer |
|---|---|
| `hdfs:///datalake/silver/transaksi/` | Silver |
| `hdfs:///datalake/bronze/pelanggan/` | Bronze (dimensi) |
| `hdfs:///datalake/gold/per_kategori/` | Gold |
| `hdfs:///datalake/gold/per_segmen/` | Gold |
| Script | `Konfigurasi-lab/app/analisis_join.py` |

## Langkah Kerja

### 1) Tinjau skrip join & agregasi

Buka `Konfigurasi-lab/app/analisis_join.py` — perhatikan:
- `broadcast` join ke tabel pelanggan kecil
- `left_anti` untuk transaksi orphan
- agregasi ke dua path Gold

### 2) Jalankan pipeline Gold (dari host)

```bash
cd sesi-praktikum/chapter-6/Konfigurasi-lab
bash scripts/run_analisis_join.sh
```

### 3) Verifikasi Gold

```bash
bash scripts/spark_exec.sh "hdfs dfs -ls -R /datalake/gold/"
bash scripts/spark_exec.sh "hdfs dfs -du -h /datalake/gold/per_kategori/"
bash scripts/verify_datalake.sh
```

## Hasil yang Dicatat

- Jumlah baris Gold per kategori dan per segmen
- Hasil anti join (transaksi orphan)
- Tabel omzet per segmen

## Refleksi Singkat

1. Mengapa `F.broadcast(df_plg)` dipakai di sini?
2. Apa manfaat `cache()` sebelum dua agregasi Gold?

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Execution Plan & Optimasi**.*
