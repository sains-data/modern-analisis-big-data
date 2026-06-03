# Instruksi — Big Data PT

## Langkah 1 — Setup

```bash
cd sesi-praktikum/chapter-17/studi-kasus-edukasi/arsitektur-lab
chmod +x *.sh scripts/*.sh
```

## Langkah 2 — Data

```bash
bash scripts/prepare_data.sh
```

500 mahasiswa anonim · LMS · absensi · lowongan kerja.

## Langkah 3 — Pipeline

```bash
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
bash scripts/verify_stack.sh
```

## Langkah 4 — Verifikasi output

| Output | File |
|---|---|
| 1 EWS PA | `output/output-1-early-warning-pa/notifikasi_pa_latest.csv` |
| 2 Ruang | `output/output-2-utilisasi-ruang/utilisasi_ruang_latest.csv` |
| 3 Skill gap | `output/output-3-skill-gap/laporan_skill_gap_latest.pdf` |
| 4 BAN-PT | `output/output-4-banpt/indikator_banpt_latest.pdf` |

## Langkah 5 — Sprint Review

- Demo PA: mahasiswa KRITIS + faktor risiko (`faktor_risiko_top5.json`)
- Cek AUC di `data/gold/model_meta.json` (target ≥ 0,75)

## Pengumpulan

Log + retrospective privasi di `eksperimen/catatan/`.
