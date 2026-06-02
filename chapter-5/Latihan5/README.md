# Latihan 5 — Eksplorasi Mandiri: Partisi dan Caching
**Chapter 5 · Apache Spark** | Estimasi waktu: **25 menit**

## Tujuan

- Menguji pengaruh jumlah partisi (`slices`) pada performa dan akurasi Pi
- Mendemonstrasikan manfaat `.cache()` pada RDD
- Menjawab pertanyaan diskusi konseptual PySpark

## Prasyarat

- [ ] Latihan 1–4 selesai
- [ ] Script `hitung_pi.py` dari Latihan 2 tersedia

## Langkah Kerja

### Bagian A — Pengaruh jumlah partisi

Gunakan env `SLICES` (skrip `app/hitung_pi.py`):

```bash
cd ../Konfigurasi-lab
SLICES=4  bash scripts/run_hitung_pi.sh
SLICES=8  bash scripts/run_hitung_pi.sh
SLICES=16 bash scripts/run_hitung_pi.sh
```

| Jumlah Dart | Slices | Nilai Pi | Waktu (detik) |
|---|---|---|---|
| 1.000.000 | 4 | | |
| 1.000.000 | 8 | | |
| 1.000.000 | 16 | | |

### Bagian B — Caching RDD

```bash
bash scripts/run_hitung_pi_cache.sh
```

Skrip: `app/hitung_pi_cache.py`. Catat waktu run 1 vs run 2 di log dan Spark UI (Storage).

## Pertanyaan Diskusi

1. Apa keuntungan `sc.parallelize()` untuk pengujian performa klaster (tanpa baca HDFS)?
2. Apa perbedaan `--deploy-mode client` vs `cluster` terhadap lokasi Driver dan log terminal?
3. Sebutkan dua perbedaan `RDD.map()` vs `DataFrame.withColumn()` dari sisi optimasi Spark.

## Penutup

Keluar dari container dan hentikan klaster jika latihan selesai:

```bash
cd ../Konfigurasi-lab
bash stop.sh
```

---

*Latihan 5 selesai. Chapter 5 praktik tuntas.*
