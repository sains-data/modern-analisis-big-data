# Katalog Data — Chapter 6

Dataset latihan **Medallion Bronze** berasal dari generator sintesis Gaussian Copula (`synthetic-data/`), entitas **`catatan_aktivitas`** + **`entitas_partisipan`**, diekspor ke format legacy lab.

## File sumber

| Path | Format | Volume | Entitas kanonik |
|------|--------|--------|-----------------|
| `data/transaksi.csv` | CSV legacy | **16 baris** (+ header) | `catatan_aktivitas` |
| `data/pelanggan.csv` | CSV legacy | **7 baris** (+ header) | `entitas_partisipan` |
| `data/catatan_aktivitas.csv` | CSV kanonik | 16 baris | `catatan_aktivitas` |
| `data/entitas_partisipan.csv` | CSV kanonik | 7 baris | `entitas_partisipan` |

## Schema legacy — `transaksi.csv`

| Kolom lab | Kolom kanonik | Tipe |
|-----------|---------------|------|
| `id_transaksi` | `id_aktivitas` (alias TRX001…) | string |
| `id_pelanggan` | `id_partisipan` (alias C001…) | string |
| `tanggal` | `tanggal` | date |
| `kategori` | `kelas_layanan` | string |
| `produk` | `nama_item` | string |
| `jumlah` | `harga_satuan` | integer/float |
| `kuantitas` | `kuantitas` | integer |
| `kota` | `unit_geografis` | string |

## Schema legacy — `pelanggan.csv`

| Kolom lab | Kolom kanonik | Tipe |
|-----------|---------------|------|
| `id_pelanggan` | `id_partisipan` (C001 = PK-0001) | string |
| `nama` | `nama` | string |
| `email` | `email` | string |
| `segmen` | `segmen` (Premium/VIP/Regular) | string |
| `tanggal_daftar` | `tanggal_bergabung` | date |

## Mapping ID partisipan

| Legacy | Kanonik | Nama |
|--------|---------|------|
| C001 | PK-0001 | Andi Saputra |
| C002 | PK-0002 | Budi Santoso |
| C003 | PK-0003 | Sari Dewi |
| C004 | PK-0004 | Ahmad Rizky |
| C005 | PK-0005 | Maria Chen |
| C006 | PK-0006 | Dewi Lestari |
| C007 | PK-0007 | Budi Hartono |

Nama dan email selaras Bab 3 (`sample_users`) dan Bab 5 (`mahasiswa.csv`).

## Anomali terkontrol (`transaksi.csv`)

| ID | Masalah | Dampak pipeline Silver |
|----|---------|------------------------|
| TRX001 | Duplikat penuh (2×) | `dropDuplicates` → 1 baris |
| TRX011 | `id_pelanggan` kosong | Ditolak validasi |
| TRX012 | `jumlah` negatif (−150.000) | Ditolak (`jumlah > 0`) |
| TRX013 | `kuantitas` = 0 | Ditolak (`kuantitas > 0`) |
| TRX014 | `kota` = `palembang` (lowercase) | **Lolos** — diperbaiki `initcap` → `Palembang` |

## Volume pipeline (harapan)

| Layer | Path HDFS | Volume |
|-------|-----------|--------|
| Bronze transaksi | `/datalake/bronze/transaksi/transaksi.csv` | **16 baris** |
| Bronze pelanggan | `/datalake/bronze/pelanggan/pelanggan.csv` | 7 baris |
| Silver transaksi | `/datalake/silver/transaksi/` | **12 baris** valid |
| Gold per_kategori | `/datalake/gold/per_kategori/` | agregat dari 12 baris |
| Gold per_segmen | `/datalake/gold/per_segmen/` | agregat dari 12 baris |

Perhitungan Silver: 16 Bronze → dedup 15 → tolak TRX011, TRX012, TRX013 → **12 valid**.

## Path HDFS

```
/datalake/
├── bronze/
│   ├── transaksi/transaksi.csv
│   └── pelanggan/pelanggan.csv
├── silver/transaksi/          ← Parquet, partisi tahun/bulan
└── gold/
    ├── per_kategori/
    └── per_segmen/
```

## Regenerasi data

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch06_medallion
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
