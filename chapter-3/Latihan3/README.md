# Latihan 3 — Transformasi Bronze ke Silver
**Chapter 3 · Desain Arsitektur dan Platform Big Data** | Estimasi waktu: **30 menit**

## Tujuan

- Membaca data mentah dari Bronze
- Melakukan pembersihan data (deduplikasi, imputasi, standarisasi)
- Menyimpan hasil ke Silver dalam format Parquet

## Prasyarat

- [ ] Latihan 2 selesai
- [ ] Object Bronze `users/sample_users.csv` tersedia

## Langkah Kerja

### 1) Skrip transformasi

File: `Konfigurasi-lab/app/transform.py` (dedup, imputasi gaji, standarisasi kolom, Parquet).

### 2) Jalankan transformasi

```bash
cd ../Konfigurasi-lab
docker exec -it bigdata-compute python transform.py
docker exec -it bigdata-mc mc ls local/silver --recursive
```

## Output yang Diharapkan

- Bronze: 6 baris
- Setelah deduplikasi: 5 baris
- Tersimpan file: `silver/users/users_clean.parquet`

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Agregasi Silver ke Gold**.*
