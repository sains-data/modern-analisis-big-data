# Eksperimen — Studi Kasus Kesehatan (Stunting Sumut)

**Mulai di sini** untuk praktikum analitik stunting.

## Titik eksekusi kode

```text
studi-kasus-kesehatan/arsitektur-lab/
```

## Dokumen

| File | Isi |
|---|---|
| [INSTRUKSI-EKSPERIMEN.md](INSTRUKSI-EKSPERIMEN.md) | Langkah 0–8 |
| [CHECKLIST-SPRINT.md](CHECKLIST-SPRINT.md) | Centang per sprint |

## Jalur cepat

```bash
cd sesi-praktikum/chapter-17/studi-kasus-kesehatan/arsitektur-lab
chmod +x *.sh scripts/*.sh
bash scripts/prepare_data.sh
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
bash scripts/verify_stack.sh
```

## Tugas di folder `eksperimen/`

- Salin `catatan/template-log-eksperimen.md` → log harian  
- Screenshot dashboard / peta di `catatan/bukti/`  
- Isi `catatan/retrospective-sprint3.md`  
- Kumpulkan checklist terisi ke dosen
