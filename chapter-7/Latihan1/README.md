# Latihan 1 — Persiapan Lingkungan & Data
**Chapter 7 · Apache Arrow** | Estimasi waktu: **20 menit**

## Tujuan

- Menyiapkan virtual environment Python dengan PyArrow, DuckDB, dan Polars
- Membuat struktur folder `data/` dan `datalake/`
- Menyiapkan dataset transaksi dan pelanggan (sama seperti Bab 6, dengan anomali)

## Prasyarat

- [ ] Setup lab — [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Python 3.10+ terpasang

## Referensi Lingkungan Lab

| Path | Peran |
|---|---|
| `Konfigurasi-lab/data/transaksi.csv` | Sumber mentah |
| `Konfigurasi-lab/data/pelanggan.csv` | Dimensi pelanggan |
| `Konfigurasi-lab/datalake/bronze/` | Output setelah Latihan 2 |
| `Konfigurasi-lab/datalake/silver/` | Output setelah Latihan 3 |
| `Konfigurasi-lab/datalake/gold/` | Output setelah Latihan 4 |

## Langkah Kerja

### 1) Setup venv & dependensi

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
bash setup.sh
bash scripts/setup_dirs.sh
```

### 2) Verifikasi data & paket

```bash
bash scripts/verify_deps.sh
```

Data CSV sudah tersedia di `data/` (15 baris transaksi + anomali). Tidak perlu `cat` manual.

### 3) Inspeksi anomali (opsional)

Buka `data/transaksi.csv` dan identifikasi duplikat TRX001, TRX011, TRX012, inkonsistensi kota.

## Anomali untuk Diuji di Pipeline

| Masalah | Contoh |
|---|---|
| Duplikasi | TRX001 |
| ID pelanggan kosong | TRX011 |
| Nilai negatif / kuantitas 0 | TRX011, TRX012 |
| Inkonsistensi kota | `JAKARTA`, `yogyakarta` |

## Refleksi Singkat

1. Mengapa pipeline Arrow ini dijalankan lokal, bukan di YARN?
2. Apa perbedaan path `data/` vs `datalake/bronze/`?

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — Bronze dengan PyArrow**.*
