# Eksperimen — Studi Kasus Lingkungan (Karhutla Riau)

**Mulai di sini.** Eksekusi kode: `../arsitektur-lab/`

| Dokumen | Isi |
|---|---|
| [INSTRUKSI-EKSPERIMEN.md](INSTRUKSI-EKSPERIMEN.md) | Langkah 0–8 |
| [CHECKLIST-SPRINT.md](CHECKLIST-SPRINT.md) | Sprint 1–3 |

```bash
cd ../arsitektur-lab
chmod +x *.sh scripts/*.sh
bash scripts/prepare_data.sh
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
```

Tugas di `eksperimen/catatan/`: log, screenshot peta H3, retrospective.
