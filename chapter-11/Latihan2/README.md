# Latihan 2 — Supervised Learning: Regresi dan Klasifikasi
**Modul 9 · Machine Learning Big Data** | Estimasi waktu: **35 menit**

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Latihan 1 selesai (data tersedia di Silver layer)

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
