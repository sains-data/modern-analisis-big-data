# Latihan 2 — Persiapan Data Analitik & Ekspor
**Chapter 12 · Visualisasi dan Eksplorasi Data** | Estimasi: **45 menit** | **Tahap 2** (Bab 12)

## Tujuan

- Membuat tiga tabel agregat Gold (`persiapan_analitik.py`)
- Menghitung **MA3**, **MoM growth**, kumulatif (`metrik_lanjutan.py`)
- Mengekspor ke PostgreSQL (`ekspor_postgresql.py`)

## Prasyarat

- [ ] Latihan 1 — Silver di `/datalake/silver/transaksi/`
- [ ] `viz-postgres` berjalan (`bash start-viz.sh`)

## Referensi buku (§12.3)

| Skrip | Output HDFS |
|---|---|
| `persiapan_analitik.py` | `gold/tren_bulanan/`, `gold/omzet_kategori/`, `gold/omzet_kota/` |
| `metrik_lanjutan.py` | `gold/tren_lanjutan/` (berisi `ma3_omzet`, `mom_growth_pct`, …) |
| `ekspor_postgresql.py` | Tabel PG: `tren_bulanan`, `omzet_kategori`, `omzet_kota` |

## Langkah kerja

### 1) Agregat dasar

```bash
cd sesi-praktikum/chapter-12/Konfigurasi-lab
bash scripts/run_persiapan_analitik.sh
```

Verifikasi:

```bash
bash scripts/spark_exec.sh "hdfs dfs -ls /datalake/gold/"
```

### 2) Metrik lanjutan (window function)

```bash
bash scripts/run_metrik_lanjutan.sh
```

Perhatikan output `show(12)` — kolom `ma3_omzet`, `mom_growth_pct`, `peringkat_omzet`.

### 3) JDBC driver & ekspor

```bash
bash scripts/install_jdbc_driver.sh
bash scripts/run_ekspor_postgresql.sh
bash scripts/verify_postgres.sh
```

Sesuaikan `PG_JDBC_URL` di `.env` jika koneksi gagal (lihat Konfigurasi-lab README).

## Tabel pencatatan (sesuai buku)

| Tabel PostgreSQL | Jumlah baris | Status |
|---|---|---|
| `tren_bulanan` | ~12 | |
| `omzet_kategori` | ~5 | |
| `omzet_kota` | ~10 | |

## Refleksi

1. Mengapa `tren_bulanan` di PostgreSQL dibaca dari path `tren_lanjutan` di HDFS?
2. Apa arti `mom_growth_pct` null pada bulan pertama?

---

*Latihan 2 selesai. Lanjut **Latihan 3 — Visualisasi Superset (Tahap 3)**.*
