# Keterangan File Data — Modul 9

Folder `Data/` berisi referensi dataset untuk dokumentasi modul. Saat praktikum, data utama dibangkitkan otomatis oleh script `Konfigurasi-lab/scripts/buat_data_ml.py`.

## Daftar File

| File | Digunakan di | Keterangan |
|---|---|---|
| `transaksi_ml.json` | Referensi skema | Sampel data transaksi format JSON |
| `transaksi_ml.csv` | Eksplorasi lokal | Versi CSV untuk preview cepat |
| `transaksi_ml_sample.json` | Referensi cepat | Cuplikan kecil untuk inspeksi format |
| `pelanggan_agregat.json` | Latihan 3 (konsep) | Contoh agregasi per pelanggan |
| `referensi_schema_modul9.json` | Semua latihan | Dokumentasi kolom dan tipe data |

## Cara pakai di lab

Jalankan dari folder `Konfigurasi-lab/`:

```bash
bash scripts/init_data.sh
```

Perintah ini akan membuat dataset latihan ke:

- `hdfs:///datalake/bronze/transaksi/`
- `hdfs:///datalake/silver/transaksi/`

## Catatan

- Dataset generator memakai `random.seed(42)` agar hasil konsisten.
- Semua latihan membaca data dari HDFS Silver layer, bukan langsung dari `Data/`.
