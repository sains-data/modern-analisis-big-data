# Analitik — Studi Kasus Lingkungan

Pipeline **batch** (NBR, join konsesi) dan **streaming** (FIRMS, ISPA), plus model risiko dan korelasi kesehatan.

## Isi yang direncanakan (Lampiran)

```
analitik/
├── batch/              # Airflow tasks: nbr, join_spasial, indeks_risiko
├── streaming/          # FIRMS H3, ISPA window
├── model/              # XGBoost prediksi 3 hari (opsional)
├── sql/                # Akuntabilitas konsesi, emisi
└── notebooks/          # Validasi CRS, Gi*, CCF
```

## Dokumentasi

→ **[PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md)**

## Metrik sukses

| Analitik | Target |
|---|---|
| Query akuntabilitas 1 tahun | &lt; 60 detik |
| Indeks risiko harian | Tersedia sebelum 06:00 WIB |
| Korelasi ISPU–ISPA | Lag optimal per kecamatan teridentifikasi |
