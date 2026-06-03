# Latihan 2 — Supervised Learning: Regresi dan Klasifikasi
**Chapter 11 · Machine Learning Big Data** | Estimasi waktu: **35 menit**

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Latihan 1 selesai (10.000 baris di Silver layer)
- [ ] Label `segmen` — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md): tinggi ~78%, menengah ~21%, rendah ~1%

## Referensi data

| Kolom | Peran |
|-------|-------|
| `total_nilai` | Target regresi |
| `segmen` | Target klasifikasi (3 kelas, tidak seimbang) |
| `kuantitas`, `harga_satuan`, `diskon`, `berat_kg`, `kategori`, `channel` | Fitur |

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Folder kerja | `Konfigurasi-lab/` |
| Script regresi | `scripts/linear_regression.py` |
| Script klasifikasi | `scripts/klasifikasi_dt.py` |
| Path input | `hdfs:///datalake/silver/transaksi/` |

## Langkah Kerja

### A. Linear Regression

```bash
cd ../Konfigurasi-lab
bash scripts/spark_submit.sh /opt/modul9/scripts/linear_regression.py
```

Catat metrik:
- RMSE
- MAE
- R²
- durasi training

### B. Logistic Regression vs Decision Tree

```bash
cd ../Konfigurasi-lab
bash scripts/spark_submit.sh /opt/modul9/scripts/klasifikasi_dt.py
```

Catat metrik:
- Accuracy
- F1
- Precision
- Recall
- Feature importance Decision Tree

## Verifikasi tambahan

```bash
open http://localhost:8088
open http://localhost:4040
```

Amati job Spark saat masing-masing script berjalan.

---

*Latihan 2 selesai. Lanjut ke **Latihan 3 — Unsupervised Learning: K-Means Clustering**.*
