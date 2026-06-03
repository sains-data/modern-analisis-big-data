# Latihan 4 — Agregasi Silver ke Gold
**Chapter 3 · Desain Arsitektur dan Platform Big Data** | Estimasi waktu: **25 menit**

## Tujuan

- Membaca data bersih dari Silver
- Melakukan agregasi analitik per kota
- Menyimpan output business-ready ke Gold

## Prasyarat

- [ ] Latihan 3 selesai
- [ ] File `silver/users/users_clean.parquet` tersedia (**50 baris**)

## Referensi agregasi

Skrip `aggregate.py` menghitung per kolom `city`:

| Metrik Gold | Kolom sumber |
|-------------|--------------|
| `avg_salary` | rata-rata `salary` |
| `total_karyawan` | jumlah baris per kota |
| `avg_usia` | rata-rata `age` |

Dataset Silver mencakup **10 kota**: Jakarta, Surabaya, Bandung, Medan, Semarang, Makassar, Palembang, Denpasar, Yogyakarta, Balikpapan.

Gold layer diharapkan berisi **10 baris** (satu ringkasan per kota).

## Langkah Kerja

### 1) Skrip agregasi

File: `Konfigurasi-lab/app/aggregate.py`

### 2) Jalankan script

```bash
cd ../Konfigurasi-lab
docker exec -it bigdata-compute python aggregate.py
```

Perhatikan tabel ringkasan 10 kota yang dicetak ke terminal.

### 3) Verifikasi output Gold

```bash
docker exec -it bigdata-mc mc ls local/gold --recursive
```

## Hasil yang Dicatat

- Tabel ringkasan per kota (salin 2–3 baris contoh)
- Key object Gold: `summary/city_summary.parquet`
- Kota dengan `total_karyawan` terbanyak
- Kota dengan `avg_salary` tertinggi

---

*Latihan 4 selesai. Lanjut ke **Latihan 5 — Validasi End-to-End dan Latihan Lanjutan**.*
