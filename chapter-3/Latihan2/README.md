# Latihan 2 — Membuat Zona Medallion dan Ingesti Bronze
**Chapter 3 · Desain Arsitektur dan Platform Big Data** | Estimasi waktu: **25 menit**

## Tujuan

- Membuat bucket `bronze`, `silver`, `gold`
- Mengunggah data mentah ke zona Bronze tanpa modifikasi

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Stack `bigdata-minio` dan `bigdata-compute` berjalan

## Langkah Kerja

### 1) Verifikasi bucket Medallion

Jika sudah menjalankan `bash start.sh`, bucket sudah dibuat. Verifikasi:

```bash
cd ../Konfigurasi-lab
docker exec -it bigdata-mc mc ls local/
```

Atau buat manual:

```bash
bash scripts/init_buckets.sh
```

### 2) Data mentah

File sudah tersedia di `Konfigurasi-lab/raw-data/sample_users.csv` (6 baris, termasuk duplikat dan null).

### 3) Upload ke Bronze

Skrip: `Konfigurasi-lab/app/upload_bronze.py`

```bash
cd ../Konfigurasi-lab
docker exec -it bigdata-compute python upload_bronze.py
docker exec -it bigdata-mc mc ls local/bronze --recursive
```

## Hasil yang Dicatat

- Daftar bucket yang berhasil dibuat
- Key object di Bronze: `users/sample_users.csv`

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Transformasi Bronze ke Silver**.*
