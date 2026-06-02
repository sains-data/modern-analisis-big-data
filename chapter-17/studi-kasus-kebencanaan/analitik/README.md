# Analitik — Studi Kasus Kebencanaan

Folder **analitik** menampung definisi pipeline, query, notebook, dan model yang menjawab tiga pertanyaan bisnis (kapan / siapa / ke mana).

## Isi yang direncanakan (Lampiran)

```
analitik/
├── streaming/           # Spark Structured Streaming — agregasi TMA + siaga
├── batch/               # Airflow + Sedona — SAR, DEM, statis
├── model/               # LSTM prediksi TMA (opsional sprint 2+)
├── sql/                 # Spatial join populasi, routing KNN
└── notebooks/           # Eksplorasi dan validasi hasil
```

Saat ini: dokumentasi dan pemetaan sprint; kode menyusul di Lampiran.

## Dokumentasi

→ **[PANDUAN-ANALITIK.md](PANDUAN-ANALITIK.md)** — alur job, cuplikan kode buku, metrik sukses, pemetaan peran Scrum.

## Metrik sukses (contoh Product Owner)

| Pertanyaan | Metrik | Target lab |
|---|---|---|
| Kapan? | RMSE prediksi TMA 6 jam | &lt; ambang disepakati tim + BPBD |
| Siapa? | Waktu spatial join populasi | &lt; 60 detik |
| Ke mana? | Rute shelter valid (tidak tergenang) | 100% shelter terhubung jalan Silver |

## Dependensi

- Lingkungan: [../arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md](../arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md)  
- Input: tabel Gold/Silver di [../data/](../data/)  
- Keluaran: artefak di [../output/](../output/)  
