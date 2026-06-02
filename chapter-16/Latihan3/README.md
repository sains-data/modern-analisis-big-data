# Latihan 3 — Spatial Join Batas Administrasi
**Chapter 16** | Estimasi: **40 menit** | **Tahap 3**

## Tujuan

- Spatial join hotspot Silver × batas kecamatan
- Membaca **physical plan** (`explain()`)
- Top 10 kecamatan dengan hotspot terbanyak

## Prasyarat

- [ ] `data/batas_kecamatan_sumatera.geoparquet` ada (`bash scripts/prepare_data.sh`)
- [ ] Silver layer dari Latihan 1

## Langkah kerja

Jalankan sel **Tahap 3** di notebook.

### 1) Periksa physical plan

Catat strategi join yang muncul:

- [ ] RangeJoin
- [ ] BroadcastIndexJoin
- [ ] CartesianProduct (tidak diinginkan)

### 2) Top kecamatan

Isi tabel dari output `show(10)`:

| nama_kecamatan | kabupaten | provinsi | n_hotspot | avg_frp |
|---|---|---|---|---|

## Refleksi

1. Mengapa `ST_SimplifyPreserveTopology` dipakai pada poligon kecamatan?
2. Apa yang terjadi jika CRS hotspot dan batas berbeda tanpa `ST_Transform`?

---

*Lanjut **Latihan 4 — Gi* (Tahap 4)**.*
