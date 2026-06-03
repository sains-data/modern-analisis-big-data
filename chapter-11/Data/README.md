# Keterangan File Data — Chapter 11

File data latihan ada di folder **`Data/`** (referensi statis). Saat praktikum, data utama di HDFS dibuat oleh `Konfigurasi-lab/scripts/init_data.sh`.

Dokumentasi lengkap: **[KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)**.

## Daftar File

| File | Volume | Digunakan di | Keterangan |
|---|---|---|---|
| `transaksi_ml.csv` | **10.000** | Eksplorasi lokal | Versi CSV |
| `transaksi_ml.json` | 10.000 | Referensi skema | Format JSON lengkap |
| `transaksi_ml_sample.json` | 100 | Inspeksi cepat | 100 record pertama |
| `pelanggan_agregat.json` | **200** | Latihan 3 (konsep) | Agregasi per `id_pelanggan` |
| `referensi_schema_modul9.json` | — | Semua latihan | Kolom, label, metrik model |

## Cara pakai di lab

Jalankan dari folder `Konfigurasi-lab/`:

```bash
bash scripts/init_data.sh
```

Perintah ini membuat dataset latihan ke:

- `hdfs:///datalake/bronze/transaksi/`
- `hdfs:///datalake/silver/transaksi/`

Semua latihan ML membaca dari **HDFS Silver**, bukan langsung dari `Data/`.

## Regenerasi data referensi

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch11_ml
bash scripts/sync_to_chapters.sh
```

## Catatan

- Referensi copula: seed **42**, `total_nilai = kuantitas × harga_satuan × (1−diskon)`
- Label `segmen` ada di file referensi; di HDFS dihitung ulang oleh script ML
- `pelanggan_agregat.json` selaras fitur K-Means: `total_trx`, `total_belanja`, `avg_belanja`, `maks_belanja`, `ragam_kategori`
