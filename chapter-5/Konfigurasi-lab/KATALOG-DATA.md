# Katalog Data — Chapter 5

Dataset latihan **`mahasiswa.csv`** berasal dari generator sintesis Gaussian Copula (`synthetic-data/`), entitas **`skor_kompetensi`**, disinkronkan ke format legacy lab via alias kolom.

## File sumber

| Path | Format | Volume | Entitas kanonik |
|------|--------|--------|-----------------|
| `data/mahasiswa.csv` | CSV (legacy lab) | **10 baris** (+ header) | `skor_kompetensi` |
| `data/skor_kompetensi.csv` | CSV (kanonik) | **10 baris** (+ header) | `skor_kompetensi` |

## Schema legacy (`mahasiswa.csv`)

| Kolom lab | Kolom kanonik | Tipe | Range |
|-----------|---------------|------|-------|
| `nim` | `id_partisipan` (alias `2021XXX`) | string | `2021001`–`2021010` |
| `nama` | `nama` | string | Pool nama partisipan |
| `nilai_uts` | `skor_modul_a` | float | 0–100 |
| `nilai_uas` | `skor_modul_b` | float | 0–100 |
| `nilai_tugas` | `skor_modul_c` | float | 0–100 |

Tiga skor di-generate **bersama-sama** via Gaussian Copula (Blok C) — korelasi positif moderat antar modul.

## Mapping ID

| `nim` (lab) | `id_partisipan` (kanonik) |
|-------------|---------------------------|
| `2021001` | `PK-0001` |
| `2021002` | `PK-0002` |
| … | … |
| `2021010` | `PK-0010` |

Nama partisipan **sama** dengan entitas di Bab 3 (`sample_users.csv`).

## Formula analisis (`analisis_nilai.py`)

```
nilai_akhir = nilai_uts × 0.30 + nilai_uas × 0.40 + nilai_tugas × 0.30
```

| Grade | Syarat |
|-------|--------|
| A | nilai_akhir ≥ 85 |
| B | ≥ 75 |
| C | ≥ 65 |
| D | ≥ 55 |
| E | < 55 |

### Distribusi grade harapan (10 partisipan)

| Grade | Jumlah |
|-------|--------|
| A | 1 |
| B | 2 |
| C | 3 |
| D | 3 |
| E | 1 |

Contoh nilai akhir tertinggi: **Ahmad Rizky** (`2021004`) — 85,3 (grade A).

## Path HDFS

| Path | Isi |
|------|-----|
| `/user/lab/modul5/mahasiswa.csv` | Input CSV |
| `/user/lab/modul5/hasil_nilai/` | Output Parquet (Latihan 3) |

## Regenerasi data

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch05_spark
bash scripts/sync_to_chapters.sh
```

Seed default: `42`.
