# Latihan 1 — Persiapan Lingkungan & Data
**Chapter 7 · Apache Arrow** | Estimasi waktu: **20 menit**

## Tujuan

- Menyiapkan virtual environment Python dengan PyArrow, DuckDB, dan Polars
- Membuat struktur folder `data/` dan `datalake/`
- Menyiapkan dataset catatan aktivitas & partisipan (identik Bab 6, anomali terkontrol)

## Prasyarat

- [ ] Setup lab — [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Python 3.10+ terpasang
- [ ] File data tersedia — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Referensi data

| File | Volume | Catatan |
|------|--------|---------|
| `data/transaksi.csv` | **16 baris** | Legacy + anomali |
| `data/pelanggan.csv` | **7 baris** | C001–C007 = PK-0001–PK-0007 |
| `data/catatan_aktivitas.csv` | 16 baris | Schema kanonik |
| `data/entitas_partisipan.csv` | 7 baris | Schema kanonik |

Dataset disinkronkan dari generator sintesis Copula (export Bab 6/7).

## Referensi Lingkungan Lab

| Path | Peran |
|---|---|
| `Konfigurasi-lab/data/transaksi.csv` | Sumber mentah |
| `Konfigurasi-lab/data/pelanggan.csv` | Dimensi partisipan |
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
wc -l data/transaksi.csv data/pelanggan.csv
```

Harapan: **17** dan **8** baris (`wc -l` termasuk header) = 16 + 7 data.

### 3) Inspeksi anomali

| ID | Anomali |
|----|---------|
| TRX001 | Duplikat (baris 1 & 16) |
| TRX011 | `id_pelanggan` kosong |
| TRX012 | `jumlah` negatif |
| TRX013 | `kuantitas` = 0 |
| TRX014 | `kota` = `palembang` (lowercase) |

## Refleksi Singkat

1. Mengapa pipeline Arrow dijalankan lokal, bukan di YARN?
2. Apa perbedaan path `data/` vs `datalake/bronze/`?
3. Apa perbedaan dedup di Bronze (Bab 7) vs Silver (Bab 6)?

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — Bronze dengan PyArrow**.*
