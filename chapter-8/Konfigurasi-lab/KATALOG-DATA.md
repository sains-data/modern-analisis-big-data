# Katalog Data — Chapter 8

Dataset latihan **skala menengah** (500 transaksi, 50 pelanggan) berasal dari generator sintesis Gaussian Copula (`synthetic-data/`), entitas **`catatan_aktivitas`** + **`entitas_partisipan`**. Tidak ada anomali terkontrol — fokus Bab 8: volume, partisi Hive, agregasi HBase, dan benchmark format.

## File sumber

| Path | Format | Volume | Entitas kanonik |
|------|--------|--------|-----------------|
| `data/transaksi.csv` | CSV legacy | **500 baris** (+ header) | `catatan_aktivitas` |
| `data/pelanggan.csv` | CSV legacy | **50 baris** (+ header) | `entitas_partisipan` |
| `data/catatan_aktivitas.csv` | CSV kanonik | 500 baris | `catatan_aktivitas` |
| `data/entitas_partisipan.csv` | CSV kanonik | 50 baris | `entitas_partisipan` |

## Schema legacy — `transaksi.csv`

| Kolom lab | Kolom kanonik | Tipe |
|-----------|---------------|------|
| `id_transaksi` | `id_aktivitas` (alias TRX-00001…) | string |
| `id_pelanggan` | `id_partisipan` (alias PLG-0001…) | string |
| `tanggal` | `tanggal` | date |
| `kategori` | `kelas_layanan` | string |
| `total_nilai` | `nilai_total` | float |
| `kota` | `unit_geografis` | string |

Perbedaan dengan Bab 6/7: tidak ada kolom `produk`, `jumlah`, `kuantitas`; nilai transaksi sudah agregat di `total_nilai`.

## Schema legacy — `pelanggan.csv`

| Kolom lab | Kolom kanonik | Tipe |
|-----------|---------------|------|
| `id_pelanggan` | `id_partisipan` (PLG-0001 = PK-0001) | string |
| `nama` | `nama` | string |
| `segmen` | `segmen` (Basic/Premium/Regular) | string |
| `kota_asal` | `unit_geografis` | string |

Perbedaan dengan Bab 6/7: tidak ada `email` / `tanggal_daftar`; segmen memakai label **Basic** (bukan VIP).

## Mapping ID partisipan

| Legacy | Kanonik | Nama (contoh) |
|--------|---------|---------------|
| PLG-0001 | PK-0001 | Andi Saputra |
| PLG-0002 | PK-0002 | Budi Santoso |
| PLG-0003 | PK-0003 | Sari Dewi |
| … | … | … |
| PLG-0020 | PK-0020 | Oki Ramadhan |
| PLG-0021–0050 | PK-0021–0050 | Pelanggan-0021 … Pelanggan-0050 |

20 pelanggan pertama memakai nama dari pool generator (selaras Bab 3 & 5); sisanya diberi label generik.

## Distribusi data (seed 42)

| Dimensi | Nilai |
|---------|-------|
| Kategori transaksi | Elektronik, Fashion, Kesehatan, Makanan, Otomotif, Olahraga (~76–92 baris/kategori) |
| Segmen pelanggan | Basic 30 · Premium 12 · Regular 8 |
| Kota | 10 unit geografis (Jakarta, Surabaya, Bandung, …) |
| Rentang `total_nilai` | ~Rp 22 ribu – ~Rp 92 juta |
| Pelanggan aktif transaksi | **49** dari 50 (PLG-0046 tanpa transaksi) |

## Volume pipeline (harapan)

| Layer | Path HDFS | Volume |
|-------|-----------|--------|
| Bronze transaksi | `/datalake/bronze/transaksi/data.csv` | **500 baris** |
| Bronze pelanggan | `/datalake/bronze/pelanggan/data.csv` | 50 baris |
| Silver transaksi | `/datalake/silver/transaksi/` | **500 baris** (unik `id_transaksi`) |
| HBase profil | `profil_pelanggan` | **49 baris** (pelanggan dengan ≥1 transaksi) |

Alur volume:

```
500 CSV Bronze → Silver Parquet (500) → Hive SQL / benchmark
                                      → HBase profil (49 agregat)
```

## Path HDFS

```
/datalake/
├── bronze/
│   ├── transaksi/data.csv
│   └── pelanggan/data.csv
├── silver/
│   ├── transaksi/              ← Parquet, partisi tahun/bulan
│   └── transaksi_orc/          ← Latihan 5
└── benchmark/                  ← Latihan 4
```

## Regenerasi data

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch08_storage
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
