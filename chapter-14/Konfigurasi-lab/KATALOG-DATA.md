# Katalog Data — Chapter 14

Dataset latihan **pipeline end-to-end** memakai volume **identik Bab 12** (**15.000 transaksi**, **300 partisipan**, **12 bulan** 2024) dari generator sintesis Gaussian Copula (`synthetic-data/`), modul **`ch14_e2e`** (mewarisi konfigurasi `ch12_viz`).

> **Dua sumber data:** file referensi statis di `data/` (seed 42, modul `ch14_e2e`) vs runtime **`seed_silver.py`** + **`pipeline_ecommerce.py`** di HDFS. Schema Silver sama; distribusi runtime uniform acak (5 kategori, 10 kota berbeda label).

## File sumber (referensi statis)

| Path | Format | Volume | Layer |
|------|--------|--------|-------|
| `data/silver_transaksi.csv` | CSV legacy | **15.000 baris** | Silver |
| `data/gold_tren_bulanan.csv` | CSV Gold | **12 baris** | Gold |
| `data/gold_tren_lanjutan.csv` | CSV Gold | **12 baris** | Gold + MA3/MoM (referensi) |
| `data/gold_omzet_kelas.csv` | CSV Gold | **6 baris** | Gold |
| `data/gold_omzet_geografis.csv` | CSV Gold | **10 baris** | Gold |
| `data/gold_segmentasi_rfm.csv` | CSV Gold | **300 baris** | Gold RFM |

Mapping kolom Silver/Gold: lihat [Bab 12 KATALOG-DATA.md](../../chapter-12/Konfigurasi-lab/KATALOG-DATA.md).

## Perbedaan Bab 14 vs Bab 12

| Aspek | Bab 12 | Bab 14 |
|-------|--------|--------|
| Pipeline Gold | `persiapan_analitik` + `metrik_lanjutan` (CSV) | **`pipeline_ecommerce.py`** (Parquet) |
| MoM / MA3 | Tabel terpisah `tren_lanjutan` | Kolom **`mom_growth`**, **`ma3_omzet`** di `tren_bulanan` |
| RFM di PostgreSQL | — | Tabel **`segmentasi_rfm`** (4 tabel PG) |
| Analitik SQL | — | **DuckDB** lokal (`analitik_duckdb.py`) |
| Format Gold HDFS | CSV | **Parquet** |

## Path HDFS (runtime lab)

```
/datalake/
├── silver/transaksi/              ← Parquet (seed_silver.py)
└── gold/
    ├── tren_bulanan/              ← 12 baris (+ mom_growth, ma3_omzet)
    ├── omzet_kategori/            ← 6 baris
    ├── omzet_kota/                ← 10 baris
    └── segmentasi_rfm/            ← ~300 baris
```

## PostgreSQL (Superset)

| Tabel PG | Sumber HDFS | Volume |
|----------|-------------|--------|
| `tren_bulanan` | `gold/tren_bulanan/` | **12** |
| `omzet_kategori` | `gold/omzet_kategori/` | **6** |
| `omzet_kota` | `gold/omzet_kota/` | **10** |
| `segmentasi_rfm` | `gold/segmentasi_rfm/` | **~300** |

## Volume pipeline (harapan)

```
15.000 Silver → Gold Parquet (12+6+10+300) → DuckDB → PostgreSQL → Superset
```

## Skrip runtime vs referensi

| Skrip | Peran |
|-------|-------|
| `app/seed_silver.py` | 15.000 baris → HDFS Silver |
| `app/pipeline_ecommerce.py` | Silver → Gold Parquet (+ RFM, MoM) |
| `app/analitik_duckdb.py` | Query OLAP lokal |
| `app/ekspor_postgresql.py` | Gold Parquet → PostgreSQL |
| `data/*.csv` | Referensi statis copula |

## Regenerasi data referensi

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch14_e2e
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
