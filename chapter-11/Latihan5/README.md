# Latihan 5 — Eksplorasi: Regularisasi, Kedalaman Pohon, dan Diskusi
**Chapter 11 · Machine Learning Big Data** | Estimasi waktu: **10 menit**

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Latihan 1–4 selesai
- [ ] Referensi schema — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Folder kerja | `Konfigurasi-lab/` |
| Eksperimen regParam | `scripts/eksplorasi_regparam.py` |
| Eksperimen maxDepth | `scripts/eksplorasi_maxdepth.py` |
| Input | `hdfs:///datalake/silver/transaksi/` |

## Langkah Kerja

### A) Pengaruh regularisasi pada Linear Regression

```bash
cd ../Konfigurasi-lab
bash scripts/spark_submit.sh /opt/modul9/scripts/eksplorasi_regparam.py
```

Catat tabel:
- regParam
- RMSE train
- RMSE test
- R² test

### B) Pengaruh `maxDepth` pada Decision Tree

```bash
cd ../Konfigurasi-lab
bash scripts/spark_submit.sh /opt/modul9/scripts/eksplorasi_maxdepth.py
```

Catat tabel:
- depth
- accuracy train/test
- F1 test
- gap overfitting
- jumlah node

## Pertanyaan diskusi

1. Pada nilai regParam mana model mulai underfit?
2. Pada depth berapa overfitting mulai terlihat jelas?
3. Bagaimana trade-off akurasi vs kompleksitas model di data ini?

---

*Latihan 5 selesai. Modul 9 tuntas.*
