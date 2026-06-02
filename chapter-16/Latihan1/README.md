# Latihan 1 — Persiapan Lingkungan & Ingest Data
**Chapter 16 · Analitik Big Data Spasial** | Estimasi: **45 menit** | **Setup + Tahap 1**

## Tujuan

- Menjalankan stack Docker (Spark + Sedona Jupyter + MinIO)
- Memverifikasi Apache Sedona (`ST_Point`)
- Membangun lapisan **Bronze** dan **Silver** hotspot FIRMS

## Prasyarat

- [ ] Docker aktif, RAM ≥ 8 GB
- [ ] [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)

## Referensi buku

- §16 Sesi Praktik — Langkah 1–9 (setup) + Tahap 1
- Notebook: `Konfigurasi-lab/notebooks/analitik_spasial.ipynb`

## Langkah kerja

### 1) Jalankan lab

```bash
cd sesi-praktikum/chapter-16/Konfigurasi-lab
cp .env.example .env
bash start.sh
bash scripts/verify_stack.sh
```

### 2) Jupyter

Buka http://localhost:8888 — token **`sedona123`**.

Buka `notebooks/analitik_spasial.ipynb` → jalankan sel **Verifikasi Sedona** dan **Tahap 1**.

### 3) Verifikasi HDFS/GeoParquet lokal

```bash
ls -la output/bronze/hotspot/ output/silver/hotspot/
```

### 4) MinIO (opsional)

Console http://localhost:9021 → bucket `geodata/raw/`.

## Catatan hasil

| Metrik | Nilai |
|---|---|
| Baris raw | ~500 |
| Baris Silver | |
| % valid | |
| Ukuran Bronze (MB) | |

## Refleksi

1. Mengapa geometri dibuat di Bronze, bukan di CSV mentah?
2. Filter mana yang paling banyak membuang baris di Silver?

---

*Lanjut **Latihan 2 — Grid H3 (Tahap 2)**.*
