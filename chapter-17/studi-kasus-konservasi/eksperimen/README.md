# Eksperimen — Studi Kasus Konservasi (KEL Leuser)

**Mulai di sini** · Eksekusi: `../arsitektur-lab/`

| Dokumen | Isi |
|---|---|
| [INSTRUKSI-EKSPERIMEN.md](INSTRUKSI-EKSPERIMEN.md) | Langkah praktikum |
| [CHECKLIST-SPRINT.md](CHECKLIST-SPRINT.md) | Sprint 1–3 |

```bash
cd ../arsitektur-lab && chmod +x *.sh scripts/*.sh
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/prepare_data.sh && bash scripts/run_pipeline.sh
```

**Etika:** jangan commit koordinat GPS presisi ke repo publik; gunakan `pergerakan_anonim.parquet` untuk demo.
