# Output — Studi Kasus Kebencanaan

Folder **output** menyimpan **artefak akhir** yang dibaca pemangku kebijakan—bukan tabel internal Gold semata. Empat output ini mengimplementasikan tiga pertanyaan analitik (kapan / siapa / ke mana) dalam bentuk operasional.

## Empat deliverable

| Folder | Output | Penerima utama |
|---|---|---|
| [output-1-level-siaga](output-1-level-siaga/) | Peringatan otomatis HIJAU–MERAH | Operator BPBD (WhatsApp/SMS) |
| [output-2-peta-terdampak](output-2-peta-terdampak/) | Peta populasi terdampak (Kepler.gl) | Kepala BPBD (web) |
| [output-3-logistik](output-3-logistik/) | Rencana distribusi logistik per shelter | Tim logistik (PDF) |
| [output-4-after-action](output-4-after-action/) | Laporan after-action pasca-banjir | Manajemen BNPB |

## Dokumentasi detail

→ **[PANDUAN-OUTPUT.md](PANDUAN-OUTPUT.md)** — SLO, format file, trigger, checklist demo sprint 3.

## Alur dari Gold ke output

```
data/gold/tma_siaga_hourly      ──► output-1 (notifikasi)
data/gold/populasi_terdampak    ──► output-2 (GeoJSON + config Kepler)
data/gold/rute_evakuasi         ──► output-3 (PDF per shelter)
semua gold + timeline kejadian  ──► output-4 (laporan evaluasi)
```

## Sprint 3 — definisi selesai

- [ ] Demo ke dosen/asisten: sensor uji → peta terbaru **≤ 5 menit** (SLO Output 2)  
- [ ] Empat folder berisi contoh artefak (bukan hanya README)  
- [ ] Retrospective terdokumentasi (terpisah, bisa di root studi kasus)  

## Menghasilkan artefak

```bash
cd ../arsitektur-lab && bash scripts/run_pipeline.sh
```

## Status

| Output | Skrip | Status |
|---|---|---|
| 1 Siaga | `output/scripts/output_01_level_siaga.py` | ✅ |
| 2 Peta | `output/scripts/output_02_export_peta.py` | ✅ |
| 3 Logistik | `output/scripts/output_03_logistik.py` | ✅ |
| 4 After-action | `output/scripts/output_04_after_action.py` | ✅ |
