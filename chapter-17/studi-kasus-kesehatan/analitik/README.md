# Analitik — Studi Kasus Kesehatan

Batch bulanan (z-score WHO, indeks risiko), streaming alert kader, analisis spasial (DBSCAN, Moran's I), dan isokron OSRM.

## Isi yang direncanakan (Lampiran)

```
analitik/
├── batch/           # DAG tasks: zscore, agregasi, indeks_risiko
├── streaming/       # output_03_alert_kader.py
├── model/           # XGBoost prediksi risiko (opsional)
├── sql/             # Prevalensi desa, regresi spasial
└── notebooks/       # Validasi LMS, Moran's I
```

## Dokumentasi

→ **[PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md)**

## Metrik

| Analitik | Target |
|---|---|
| Alert upload → kader | &lt; 30 detik |
| Consumer lag | &lt; 5 event |
| Isokron | 100% desa, tidak null |
