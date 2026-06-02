# Latihan 2 — Analitik SQL dengan DuckDB
**Chapter 14** | Estimasi: **35 menit** | **Tahap 2**

## Tujuan

- Mengekspor Parquet Gold dari HDFS ke lokal
- Menjalankan empat query OLAP (`analitik_duckdb.py`)
- Mencatat temuan bisnis (MoM, ranking kategori, profil RFM)

## Prasyarat

- [ ] Latihan 1 selesai — Gold Parquet di HDFS

## Referensi

- Skrip: `Konfigurasi-lab/app/analitik_duckdb.py`
- Data lokal: `Konfigurasi-lab/data/gold/`

## Langkah kerja

### 1) Ekspor dari HDFS (otomatis jika kosong)

```bash
cd sesi-praktikum/chapter-14/Konfigurasi-lab
bash scripts/export_gold_local.sh
ls -la data/gold/tren_bulanan/
```

### 2) DuckDB

```bash
bash scripts/run_analitik_duckdb.sh
```

### 3) Isi tabel temuan (buku)

| Temuan | Nilai | Interpretasi |
|---|---|---|
| Bulan omzet tertinggi | | |
| MoM growth tertinggi | % | |
| Kategori peringkat 1 | | |
| Segmen Champion (n) | | |
| Segmen At Risk (n) | | |

## Refleksi

1. Bagaimana DuckDB menggantikan Trino di lab ini?
2. Kapan federated query Trino lebih unggul daripada menyalin Parquet ke disk lokal?

---

*Lanjut **Latihan 3 — Dashboard Superset (Tahap 3)**.*
