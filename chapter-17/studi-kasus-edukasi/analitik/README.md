# Analitik — Studi Kasus Edukasi

Pipeline **batch** (fitur LA, model risiko, skill gap) dan **streaming** (LMS + alert absensi).

## Struktur

```
analitik/
├── README.md
├── PANDUAN-ANALITIK.md
├── streaming/       # Kafka → fitur harian, alert absen
├── batch/           # fitur_la, model_risiko, skill_gap
├── model/           # artefak XGBoost (Lampiran)
├── sql/             # agregasi kinerja MK, utilisasi
└── notebooks/       # eksplorasi SHAP, klaster MK
```

## Skrip referensi (buku)

| File | Fungsi |
|---|---|
| `analitik_01_fitur_la.py` | 47 fitur learning analytics |
| `analitik_02_model_risiko.py` | Train/inferensi XGBoost + SHAP |
| `analitik_03_skill_gap.py` | NLP TF-IDF lowongan vs kurikulum |

## Dokumentasi

→ **[PANDUAN-ANALITIK.md](PANDUAN-ANALITIK.md)**

## Status

Dokumentasi ✅ · Kode 🔜 Lampiran
