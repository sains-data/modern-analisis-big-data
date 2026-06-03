# Latihan 2 — Membuat Zona Medallion dan Ingesti Bronze
**Chapter 3 · Desain Arsitektur dan Platform Big Data** | Estimasi waktu: **25 menit**

## Tujuan

- Membuat bucket `bronze`, `silver`, `gold`
- Mengunggah data mentah ke zona Bronze tanpa modifikasi

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Stack `bigdata-minio` dan `bigdata-compute` berjalan

## Referensi data

| Item | Nilai |
|------|-------|
| File | `Konfigurasi-lab/raw-data/sample_users.csv` |
| Volume | **51 baris** (+ header) |
| Sumber | Generator sintesis Copula — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md) |
| Kolom | `id`, `name`, `age`, `city`, `salary`, `join_date` |

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

### 2) Eksplorasi data mentah

Buka `Konfigurasi-lab/raw-data/sample_users.csv` dan catat:

- Total **51 baris** data
- **10 kota** berbeda di kolom `city`
- Baris **3** (`Sari Dewi`): kolom `salary` kosong
- Baris **5** dan **51** (`Maria Chen`): isi identik (duplikat)

Anomali ini akan diproses di Latihan 3.

### 3) Upload ke Bronze

Skrip: `Konfigurasi-lab/app/upload_bronze.py`

```bash
cd ../Konfigurasi-lab
docker exec -it bigdata-compute python upload_bronze.py
docker exec -it bigdata-mc mc ls local/bronze --recursive
```

Output skrip harus menampilkan: *Data mentah tersimpan di Bronze layer*.

## Hasil yang Dicatat

- Daftar bucket yang berhasil dibuat
- Key object di Bronze: `users/sample_users.csv`
- Konfirmasi 51 baris terunggah (cek ukuran object atau preview via Console)

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Transformasi Bronze ke Silver**.*
