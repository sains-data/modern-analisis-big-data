# Latihan 3 — Membuat Visualisasi di Superset
**Chapter 12 · Visualisasi dan Eksplorasi Data** | Estimasi: **40 menit** | **Tahap 3** (Bab 12)

## Tujuan

- Mendaftarkan koneksi database **Analitik E-Commerce**
- Mendaftarkan dataset `tren_bulanan`, `omzet_kategori`, `omzet_kota`
- Membuat empat chart sesuai buku

## Prasyarat

- [ ] Latihan 2 — tabel PostgreSQL terisi
- [ ] Superset: http://localhost:8088 (`admin` / `admin`)
- [ ] Schema tabel — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Dataset Superset

| Tabel PG | Baris | Chart utama |
|----------|-------|-------------|
| `tren_bulanan` | 12 | Line (omzet + MA3) |
| `omzet_kategori` | 6 | Bar / Donut |
| `omzet_kota` | 10 | Table ranking |

## Langkah kerja (sesuai §12-prak-3)

### 3.1 Database connection

**Settings → Database Connections → + Database → PostgreSQL**

| Field | Nilai |
|---|---|
| Display Name | `Analitik E-Commerce` |
| Host | `postgres` |
| Port | `5432` |
| Database | `analytics` |
| Username / Password | `superset` / `superset` |

**Test Connection** → **Connect**

### 3.2 Dataset

**Data → Datasets → + Dataset** — daftarkan:

- `tren_bulanan` — tandai kolom `periode` sebagai **temporal**
- `omzet_kategori`
- `omzet_kota`

### 3.3 Chart: Bar — `Omzet per Kategori`

- Dataset: `omzet_kategori`
- Tipe: **Bar Chart**
- Metric: `SUM(omzet_total)` · Dimension: `kategori` · Sort: omzet desc
- **Save** → `Omzet per Kategori`

### 3.4 Chart: Line — `Tren Omzet Bulanan + MA3`

- Dataset: `tren_bulanan`
- Tipe: **Line Chart**
- Time: `periode` · Metrics: `SUM(omzet)` dan `AVG(ma3_omzet)`
- **Save** → `Tren Omzet Bulanan + MA3`

### 3.5 Chart: Big Number — `Total Omzet`

- Dataset: `tren_bulanan`
- Tipe: **Big Number with Trendline**
- Metric: `SUM(omzet)` · Time: `periode`
- **Save** → `Total Omzet`

### 3.6 Chart: Table — `Ranking Kota`

- Dataset: `omzet_kota`
- Kolom: `kota`, `omzet`, `transaksi`, `pelanggan_unik`, `avg_nilai`
- Conditional formatting pada `omzet`
- **Save** → `Ranking Kota`

## Pengamatan (isi dari buku)

| Pengamatan | Nilai |
|---|---|
| Kategori omzet tertinggi | |
| Bulan omzet tertinggi | |
| MoM growth tertinggi | |
| Total omzet 2024 | |

## Refleksi

1. Mengapa `ma3_omzet` ditampilkan sebagai series kedua di Line Chart?
2. Chart mana yang paling cocok untuk KPI ringkasan?

---

*Latihan 3 selesai. Lanjut **Latihan 4 — Dashboard (Tahap 4)**.*
