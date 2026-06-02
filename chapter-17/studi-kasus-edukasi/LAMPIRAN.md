# Lampiran Praktikum — Studi Kasus Edukasi

## Rencana isi Lampiran

| Komponen | Target folder |
|---|---|
| Docker: Kafka, Spark, MinIO, Superset | `arsitektur-lab/` |
| Sample SIA, LMS events, absensi (anonim) | `data/sumber/` |
| `analitik_01_fitur_la.py`, `analitik_02_model_risiko.py` | `analitik/batch/` |
| Streaming LMS + alert absen | `analitik/streaming/` |
| `analitik_03_skill_gap.py` | `analitik/batch/` |
| Dashboard Superset PA + BAN-PT | `output/` |

## Wajib sebelum Sprint 1

- Kebijakan anonimisasi `mahasiswa_id` (SHA-256 + salt institusi).  
- Daftar pengguna akhir & RBAC Gold layer.

## Versi

| Versi | Tanggal | Catatan |
|---|---|---|
| 0.1 | 2026-05 | Kerangka dokumentasi |
