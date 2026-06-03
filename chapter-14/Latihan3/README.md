# Latihan 3 — Dashboard End-to-End di Superset
**Chapter 14** | Estimasi: **45 menit** | **Tahap 3**

## Tujuan

- Mengekspor Gold ke PostgreSQL (termasuk `segmentasi_rfm`)
- Membuat chart **Pie** distribusi RFM dan **Line** MoM growth
- Mengintegrasikan ke dashboard `Analitik E-Commerce 2024` (Bab 12)

## Prasyarat

- [ ] Latihan 1–2 selesai
- [ ] Superset aktif (`bash start-viz.sh`)
- [ ] Schema PG — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Tabel PostgreSQL (harapan)

| Tabel | Baris |
|-------|-------|
| `tren_bulanan` | 12 |
| `omzet_kategori` | 6 |
| `omzet_kota` | 10 |
| `segmentasi_rfm` | ~300 |

## Langkah kerja

### 1) Stack visualisasi

```bash
cd sesi-praktikum/chapter-14/Konfigurasi-lab
bash start-viz.sh
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8088/health
```

Login: http://localhost:8088 — `admin` / `admin`

### 2) Ekspor JDBC

```bash
bash scripts/run_ekspor_postgresql.sh
bash scripts/verify_postgres.sh
```

Harus ada 4 tabel: `tren_bulanan`, `omzet_kategori`, `omzet_kota`, `segmentasi_rfm`.

### 3) Dataset Superset

**Data → Datasets → + Dataset** — database `PostgreSQL` / schema `public`:

- `segmentasi_rfm` (baru)
- `tren_bulanan` (perbarui jika sebelumnya dari `tren_lanjutan` Bab 12)

### 4) Chart

| Chart | Dataset | Tipe | Konfigurasi |
|---|---|---|---|
| Distribusi Segmen Pelanggan | `segmentasi_rfm` | Pie | Dimension: `segmen_rfm`, Metric: `COUNT(*)` |
| MoM Growth Rate (%) | `tren_bulanan` | Line | X: `periode`, Metric: `AVG(mom_growth)`, reference line di 0 |

### 5) Dashboard

Buka dashboard **Analitik E-Commerce 2024** → tambahkan kedua chart → layout F-shape.

## Catatan hasil

| Item | Status |
|---|---|
| Tabel `segmentasi_rfm` di PG | |
| Chart Pie tersimpan | |
| Chart Line MoM tersimpan | |
| Dashboard diperbarui | |

---

*Lanjut **Latihan 4 — Evaluasi Dashboard (Tahap 4)**.*
