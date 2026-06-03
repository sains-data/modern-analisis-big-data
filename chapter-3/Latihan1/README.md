# Latihan 1 — Setup Lingkungan dan Verifikasi Stack
**Chapter 3 · Desain Arsitektur dan Platform Big Data** | Estimasi waktu: **20 menit**

## Tujuan

- Menjalankan lab berbasis Docker untuk data lake
- Memverifikasi MinIO API, MinIO Console, dan compute container berjalan

## Prasyarat

- [ ] Ikuti [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Docker aktif di mesin lokal
- [ ] File `raw-data/sample_users.csv` tersedia (51 baris sintesis — lihat [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md))

## Langkah Kerja

### 1) Jalankan stack

```bash
cd ../Konfigurasi-lab
bash start.sh
docker compose ps
```

### 2) Verifikasi service

Pastikan container berikut status `Up`:
- `bigdata-minio`
- `bigdata-compute`

### 3) Verifikasi MinIO

- Buka `http://localhost:9001`
- Login `admin / admin123`

### 4) Verifikasi jaringan antar-container

```bash
docker exec -it bigdata-compute python -c "import boto3; print('boto3 OK')"
docker exec -it bigdata-mc mc alias set local http://minio:9000 admin admin123
docker exec -it bigdata-mc mc ls local/
```

## Hasil yang Dicatat

- Status `docker compose ps`
- Screenshot atau catatan akses MinIO Console
- Daftar bucket yang ada

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — Membuat Zona Medallion dan Ingesti Bronze**.*
