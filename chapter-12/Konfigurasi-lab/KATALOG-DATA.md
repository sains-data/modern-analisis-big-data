# Katalog Data — Chapter 12

Dataset latihan visualisasi (**15.000 transaksi**, **300 partisipan**, **12 bulan** 2024) berasal dari generator sintesis Gaussian Copula (`synthetic-data/`), entitas **`catatan_aktivitas`**, diekspor ke format legacy Silver + Gold CSV.

> **Dua sumber data:** file referensi statis di `data/` (seed 42) vs **`buat_data_viz.py`** runtime di HDFS (seed 42, distribusi uniform + efek musiman). Pipeline Superset membaca HDFS/PostgreSQL, bukan file lokal.

## File sumber

| Path | Format | Volume | Layer |
|------|--------|--------|-------|
| `data/silver_transaksi.csv` | CSV legacy | **15.000 baris** (+ header) | Silver |
| `data/gold_tren_bulanan.csv` | CSV Gold | **12 baris** | Gold |
| `data/gold_tren_lanjutan.csv` | CSV Gold | **12 baris** | Gold + MA3/MoM |
| `data/gold_omzet_kelas.csv` | CSV Gold | **6 baris** | Gold |
| `data/gold_omzet_geografis.csv` | CSV Gold | **10 baris** | Gold |
| `data/gold_segmentasi_rfm.csv` | CSV Gold | **300 baris** | Gold RFM |

## Schema Silver — `silver_transaksi.csv`

| Kolom lab | Kolom kanonik | Tipe |
|-----------|---------------|------|
| `id_transaksi` | `id_aktivitas` (8 char) | string |
| `id_pelanggan` | `id_partisipan` (`usr-0001` = `PK-0001`) | string |
| `kategori` | `kelas_layanan` | string |
| `channel` | `saluran` | string |
| `kota` | `unit_geografis` | string |
| `kuantitas` | `kuantitas` | integer |
| `harga_satuan` | `harga_satuan` | double |
| `diskon` | `rasio_penyesuaian` | double |
| `total_nilai` | `nilai_total` | double |
| `tahun`, `bulan`, `tanggal` | partisi waktu | int / date |

## Tabel Gold (referensi)

| File | Isi | Volume |
|------|-----|--------|
| `gold_tren_bulanan` | Omzet, jumlah transaksi, pelanggan aktif per bulan | 12 bulan |
| `gold_tren_lanjutan` | + `ma3_omzet`, `mom_growth_pct`, `kumulatif_omzet`, `peringkat_omzet` | 12 bulan |
| `gold_omzet_kelas` | Omzet per kategori + `persen_omzet` | 6 kategori |
| `gold_omzet_geografis` | Omzet per kota | 10 kota |
| `gold_segmentasi_rfm` | RFM per partisipan (`PK-XXXX`) | 300 baris |

Mapping HDFS runtime (Spark):

| Referensi CSV | Path HDFS (lab) |
|---------------|-----------------|
| `gold_tren_bulanan` | `/datalake/gold/tren_bulanan/` |
| `gold_tren_lanjutan` | `/datalake/gold/tren_lanjutan/` |
| `gold_omzet_kelas` | `/datalake/gold/omzet_kategori/` |
| `gold_omzet_geografis` | `/datalake/gold/omzet_kota/` |

PostgreSQL (setelah `ekspor_postgresql.py`):

| Tabel PG | Sumber HDFS |
|----------|-------------|
| `tren_bulanan` | `gold/tren_lanjutan/` |
| `omzet_kategori` | `gold/omzet_kategori/` |
| `omzet_kota` | `gold/omzet_kota/` |

## Distribusi data (referensi statis, seed 42)

| Dimensi | Nilai |
|---------|-------|
| Transaksi Silver | 15.000 |
| Partisipan | 300 (`usr-0001` … `usr-0300`) |
| Periode | Jan–Des 2024 (12 bulan) |
| Kategori | ~2.400–2.550 baris per kelas (6 kelas) |
| Kota | 10 unit geografis |
| RFM segmen | Champion, Loyal, Regular, At Risk |

## Volume pipeline (harapan)

```
15.000 Silver → Gold agregat (12+6+10+300) → tren_lanjutan (12) → PostgreSQL → Superset
```

## Skrip runtime vs referensi

| Skrip | Peran |
|-------|-------|
| `app/buat_data_viz.py` | Generate 15.000 baris → HDFS Silver |
| `app/persiapan_analitik.py` | Silver → Gold dasar |
| `app/metrik_lanjutan.py` | `tren_bulanan` → `tren_lanjutan` (MA3, MoM) |
| `app/ekspor_postgresql.py` | Gold HDFS → PostgreSQL |
| `data/*.csv` | Referensi statis copula |

## Regenerasi data referensi

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch12_viz
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
