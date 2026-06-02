# Latihan 4 — Agregasi Silver ke Gold
**Chapter 3 · Desain Arsitektur dan Platform Big Data** | Estimasi waktu: **25 menit**

## Tujuan

- Membaca data bersih dari Silver
- Melakukan agregasi analitik
- Menyimpan output business-ready ke Gold

## Prasyarat

- [ ] Latihan 3 selesai
- [ ] File `silver/users/users_clean.parquet` tersedia

## Langkah Kerja

### 1) Skrip agregasi

File: `Konfigurasi-lab/app/aggregate.py` (ringkasan per kota → Parquet Gold).

### 2) Jalankan script

```bash
cd ../Konfigurasi-lab
docker exec -it bigdata-compute python aggregate.py
```

### 3) Verifikasi output Gold

```bash
docker exec -it bigdata-mc mc ls local/gold --recursive
```

## Hasil yang Dicatat

- Tabel ringkasan per kota
- Key object Gold: `summary/city_summary.parquet`

---

*Latihan 4 selesai. Lanjut ke **Latihan 5 — Validasi End-to-End dan Latihan Lanjutan**.*
