# Latihan 3 — Transformasi Bronze ke Silver
**Chapter 3 · Desain Arsitektur dan Platform Big Data** | Estimasi waktu: **30 menit**

## Tujuan

- Membaca data mentah dari Bronze
- Melakukan pembersihan data (deduplikasi, imputasi, standarisasi)
- Menyimpan hasil ke Silver dalam format Parquet

## Prasyarat

- [ ] Latihan 2 selesai
- [ ] Object Bronze `users/sample_users.csv` tersedia (51 baris)

## Referensi transformasi

Skrip `transform.py` menerapkan:

| Langkah | Operasi | Dampak pada dataset |
|---------|---------|---------------------|
| 1 | `drop_duplicates()` | Baris 51 (duplikat Maria Chen) dihapus → **50 baris** |
| 2 | `fillna(median)` | `salary` baris 3 (Sari Dewi) diisi median gaji |
| 3 | Standarisasi kolom | Lowercase, strip whitespace |
| 4 | `to_datetime` | Kolom `join_date` |
| 5 | Metadata | Tambah `processed_at`, `source` |

## Langkah Kerja

### 1) Skrip transformasi

File: `Konfigurasi-lab/app/transform.py`

### 2) Jalankan transformasi

```bash
cd ../Konfigurasi-lab
docker exec -it bigdata-compute python transform.py
docker exec -it bigdata-mc mc ls local/silver --recursive
```

### 3) Verifikasi jumlah baris

Output terminal harus menunjukkan:

```
Bronze: 51 baris, 6 kolom
Silver: 50 baris setelah transformasi
```

## Output yang Diharapkan

| Layer | Volume | File |
|-------|--------|------|
| Bronze (input) | 51 baris | `bronze/users/sample_users.csv` |
| Silver (output) | **50 baris** | `silver/users/users_clean.parquet` |

## Pertanyaan refleksi

- Mengapa duplikat baris 5/51 hilang setelah `drop_duplicates()`?
- Berapa nilai median yang mengisi `salary` Sari Dewi?
- Apa keuntungan menyimpan Silver sebagai Parquet, bukan CSV?

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Agregasi Silver ke Gold**.*
