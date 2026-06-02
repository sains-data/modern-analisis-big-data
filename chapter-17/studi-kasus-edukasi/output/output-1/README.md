# Output 1 — Early Warning System (Dosen PA)

## Tujuan

Memberi dosen **Pembimbing Akademik** daftar mingguan mahasiswa bimbingan berisiko **KRITIS** atau **TINGGI**, dengan skor dan faktor risiko (SHAP) untuk intervensi dini.

## Sumber data

| Tabel | Field kunci |
|---|---|
| `gold.profil_risiko_mahasiswa` | `mahasiswa_id`, `prob_risiko`, `tingkat_risiko` |
| `silver.bimbingan_akademik` | `dosen_pa_id`, `email_pa` |

## Artefak

| Artefak | Lokasi (rencana) |
|---|---|
| Parquet notifikasi | `gold/notifikasi_pa_mingguan/` |
| Dashboard Superset | Dataset per PA, filter RLS |
| Email ringkasan | `n_kritis`, `n_tinggi` per dosen |

## Jadwal

**Mingguan** — Senin 07:00 (Airflow).

## Skrip referensi

`output_01_early_warning.py` (buku Bab 17).

## Impak kebijakan

Mengurangi angka DO dengan intervensi sebelum akhir semester; selaras permintaan Rektor pada skenario awal.
