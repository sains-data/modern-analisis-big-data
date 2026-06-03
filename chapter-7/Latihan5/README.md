# Latihan 5 — Validasi Pipeline & Eksplorasi Mandiri
**Chapter 7 · Apache Arrow** | Estimasi waktu: **25 menit**

## Tujuan

- Mengaudit jumlah baris dan skema lintas lapisan Medallion
- Memverifikasi konsistensi omzet Silver vs Gold
- Membandingkan karakteristik pipeline Arrow vs Spark (Bab 6)

## Prasyarat

- [ ] Latihan 1–4 selesai — Bronze, Silver, Gold tersedia

## Referensi Lingkungan Lab

| Script | Fungsi |
|---|---|
| `Konfigurasi-lab/app/validasi_pipeline.py` | Audit baris, skema, omzet, ukuran file |

## Langkah Kerja

### 1) Jalankan audit

```bash
cd sesi-praktikum/chapter-7/Konfigurasi-lab
bash scripts/run_validasi.sh
```

Atau pipeline penuh sekaligus:

```bash
bash scripts/run_pipeline.sh
```

### 2) Eksplorasi mandiri (opsional)

**A — Baca Gold dengan DuckDB SQL:**

```bash
source .venv/bin/activate
cd app
python -c "
import duckdb
duckdb.sql(\"\"\"
    SELECT * FROM read_parquet('../datalake/gold/per_kategori.parquet')
    ORDER BY omzet_total DESC
\"\"\").show()
"
```

**B — Bandingkan dengan Bab 6:**

| Metrik | Bab 6 (Spark/HDFS) | Bab 7 (Arrow lokal) |
|--------|-------------------|---------------------|
| Baris Silver | 12 | 12 |
| Dedup di | Silver | Bronze |
| Storage | `/datalake/` HDFS | `datalake/` lokal |

Catat startup time dan ukuran output.

## Tabel Pencatatan

| Metrik | Harapan | Nilai Anda |
|---|---|---|
| Baris Bronze | 15 | |
| Baris Silver | **12** | |
| % baris ditolak (Silver) | 20% | |
| Omzet Silver | (dari audit) | |
| Omzet Gold (sum per_kategori) | = Omzet Silver | |
| Status konsistensi | OK | |
| Ukuran Bronze / Silver / Gold (byte) | |

## Pertanyaan Diskusi

1. Pada tahap mana terjadi zero-copy yang sesungguhnya vs salinan data?
2. Jika `omzet_silver ≠ omzet_gold`, sebutkan tiga kemungkinan penyebab.
3. Kapan pipeline Arrow-only lebih tepat daripada Spark-only Medallion?
4. Apa kesamaan lazy evaluation Polars dengan Spark DataFrame?

---

*Latihan 5 selesai. Chapter 7 praktik tuntas.*
