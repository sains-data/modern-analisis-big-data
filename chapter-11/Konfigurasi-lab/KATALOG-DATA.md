# Katalog Data — Chapter 11

Dataset latihan **Machine Learning** (**10.000 transaksi**, **200 partisipan**) berasal dari generator sintesis Gaussian Copula (`synthetic-data/`), entitas **`catatan_aktivitas`**, diekspor ke format legacy ML.

> **Dua sumber data:** file referensi statis di `Data/` (seed 42) vs **`buat_data_ml.py`** runtime di HDFS (seed 42, distribusi uniform acak). Schema sama; nilai numerik berbeda dari referensi copula.

## File sumber

| Path | Format | Volume | Entitas kanonik |
|------|--------|--------|-----------------|
| `Data/transaksi_ml.csv` | CSV legacy | **10.000 baris** (+ header) | `catatan_aktivitas` |
| `Data/transaksi_ml.json` | JSON legacy | 10.000 record | `catatan_aktivitas` |
| `Data/transaksi_ml_sample.json` | JSON legacy | 100 record | subset inspeksi |
| `Data/pelanggan_agregat.json` | JSON agregat | **200 record** | agregasi per partisipan |
| `Data/referensi_schema_modul9.json` | JSON schema | — | dokumentasi kolom & model |

## Schema legacy — `transaksi_ml`

| Kolom lab | Kolom kanonik | Tipe | Catatan |
|-----------|---------------|------|---------|
| `id_transaksi` | `id_aktivitas` (8 char) | string | Unik per baris |
| `id_pelanggan` | `id_partisipan` (`usr-0001` = `PK-0001`) | string | 200 partisipan |
| `kategori` | `kelas_layanan` | string | 6 kategori |
| `channel` | `saluran` | string | mobile, web, atm, teller |
| `kuantitas` | `kuantitas` | integer | 1–20 |
| `harga_satuan` | `harga_satuan` | double | Rp |
| `diskon` | `rasio_penyesuaian` | double | 0.0–0.3 |
| `total_nilai` | `nilai_total` | double | `kuantitas × harga_satuan × (1−diskon)` |
| `berat_kg` | `berat_unit` | double | kg |
| `segmen` | label derivasi | string | Dari `total_nilai` (lihat bawah) |

## Label derivasi — `segmen`

| Kelas | Aturan (`total_nilai`) | Tipe tugas |
|-------|------------------------|------------|
| `rendah` | < Rp 100.000 | Klasifikasi (minoritas) |
| `menengah` | Rp 100.000 – < Rp 1.000.000 | Klasifikasi |
| `tinggi` | ≥ Rp 1.000.000 | Klasifikasi (mayoritas) |

Di HDFS Silver, kolom `segmen` **tidak disimpan** — dihitung ulang di script ML (`withColumn`).

## Agregasi pelanggan — `pelanggan_agregat.json`

Fitur K-Means (Latihan 3), dihitung dari 10.000 transaksi:

| Kolom | Definisi |
|-------|----------|
| `total_trx` | Jumlah transaksi per `id_pelanggan` |
| `total_belanja` | Σ `total_nilai` |
| `avg_belanja` | Rata-rata `total_nilai` |
| `maks_belanja` | Maksimum `total_nilai` |
| `ragam_kategori` | `countDistinct(kategori)` |

Volume: **200 baris** (= 200 partisipan unik).

## Distribusi data (referensi statis, seed 42)

| Dimensi | Nilai (approx.) |
|---------|-----------------|
| Transaksi | 10.000 |
| Partisipan | 200 (`usr-0001` … `usr-0200`) |
| Segmen | tinggi ~78% · menengah ~21% · rendah ~1% |
| Kategori | ~1.600–1.700 baris per kelas (6 kelas) |
| Saluran | ~2.500 baris per channel (4 saluran) |

Kelas tidak seimbang — relevan untuk diskusi Precision/Recall di Latihan 2.

## Path HDFS (runtime lab)

```
/datalake/
├── bronze/transaksi/          ← Parquet (init_data.sh)
├── silver/transaksi/          ← input semua script ML
├── gold/segmentasi_pelanggan/ ← output K-Means
├── gold/prediksi_segmen/      ← output pipeline E2E
/models/segmentasi_dt/v1/      ← model Decision Tree tersimpan
```

## Skrip runtime vs referensi

| Skrip | Peran | Output |
|-------|-------|--------|
| `scripts/buat_data_ml.py` | `init_data.sh` → HDFS | 10.000 baris Parquet (tanpa `segmen`) |
| `Data/transaksi_ml.*` | Referensi statis / eksplorasi lokal | CSV/JSON dengan `segmen` |

## Regenerasi data referensi

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch11_ml
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
