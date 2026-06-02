# Output 3 — Laporan Skill Gap & Revisi Kurikulum

## Tujuan

Memetakan skill yang **sering diminta industri** tetapi **kurang terwakili** dalam CPL/kurikulum, plus rekomendasi mata kuliah untuk penyisipan topik.

## Isi laporan

| Bagian | Deskripsi |
|---|---|
| Top skill gap | Kata/skill + `frekuensi_pct` di lowongan |
| Rekomendasi MK | `matkul_rekomendasi`, `skor_relevansi` (cosine TF-IDF) |
| Validasi | Tanda tangan Kaprodi (Sprint 3) |

## Sumber data

`gold.skill_gap_kurikulum`, `bronze/kurikulum/cpl_matkul.csv`, `silver/tfidf_*`.

## Jadwal

**Tahunan** — mendukung Evaluasi Kurikulum & siklus akreditasi BAN-PT (4 tahun).

## Skrip referensi

`output_03_laporan_skill_gap.py`.

## Impak kebijakan

Kurikulum berbasis bukti; peningkatan relevansi lulusan terhadap pasar kerja TI/data.
