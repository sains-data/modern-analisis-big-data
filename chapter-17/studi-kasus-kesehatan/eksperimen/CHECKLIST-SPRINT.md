# Checklist — Stunting Sumut

## Prasyarat

- [ ] Python 3.10+
- [ ] Baca INSTRUKSI Langkah 0–1
- [ ] Log eksperimen dibuat di `catatan/`

## Sprint 1

- [ ] `who_lms_tb_u.csv`, `desa_sumut.geojson`, `eppgbm_202605.csv`
- [ ] Dokumen 5 dimensi indeks + bobot (lihat `analitik/lib/config.py`)
- [ ] Validasi z-score 10 sampel manual

## Sprint 2

- [ ] `gold/prevalensi_stunting.parquet`
- [ ] `gold/skor_aksesibilitas` — 0 desa null waktu tempuh
- [ ] `gold/prioritas_desa_bulanan` — top 50 per kab
- [ ] Alert kader ≥ 1 event MERAH/ORANYE/KUNING
- [ ] `verify_stack.sh` semua OK

## Sprint 3

- [ ] CSV prioritas + GeoJSON desa
- [ ] `tren_provinsi.json` vs target 14%
- [ ] PDF nakes + screenshot bukti
- [ ] Retrospective + privasi data balita dibahas

## Opsional

- [ ] Kafka upload → alert &lt; 30 dtk (ukur manual)
