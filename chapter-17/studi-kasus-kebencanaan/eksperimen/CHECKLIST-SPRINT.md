# Checklist Eksperimen — per Sprint

Centang (`[x]`) setelah selesai. Simpan salinan ini di `catatan/` jika tim memerlukan versi terisi.

---

## Prasyarat

- [ ] Python 3.10+ terpasang (`python3 --version`)
- [ ] Terminal berada di `arsitektur-lab/` saat menjalankan pipeline
- [ ] Sudah membaca [INSTRUKSI-EKSPERIMEN.md](INSTRUKSI-EKSPERIMEN.md) Langkah 0–1
- [ ] File log dibuat: `catatan/log-eksperimen-YYYYMMDD.md`

---

## Sprint 1 — Data & Bronze/Silver

**Eksekusi:** `bash scripts/prepare_data.sh` (+ otomatis `ingest_static` saat pipeline)

- [ ] `data/sumber/kelurahan_sumsel.geojson` ada (50 kelurahan)
- [ ] `data/sumber/genangan_aktif.geojson` ada (2 poligon)
- [ ] `data/sumber/shelter_kapasitas.geojson` ada (5 shelter)
- [ ] `data/sumber/sensor/tma_musi/tma_readings.jsonl` ada
- [ ] `data/bronze/*.parquet` terbentuk setelah ingest
- [ ] `data/silver/kelurahan_sumsel.parquet` terbentuk
- [ ] Tiga pertanyaan analitik dipahami tim (kapan / siapa / ke mana)
- [ ] Catatan Sprint 1 ditulis di log eksperimen

---

## Sprint 2 — Pipeline & analitik

**Eksekusi:** `export PYTHONPATH=..` + `bash scripts/run_pipeline.sh`

- [ ] `data/gold/tma_siaga_hourly.parquet` ada
- [ ] `data/gold/tma_latest.parquet` — stasiun KAYU_AGUNG siaga ≥ ORANYE
- [ ] `data/gold/populasi_terdampak.parquet` — total estimasi > 0
- [ ] `data/gold/rute_evakuasi.parquet` — ≥ 1 rute ke shelter
- [ ] `bash scripts/verify_stack.sh` — semua `[OK]` (Gold)
- [ ] Tim memahami logika `analitik/lib/siaga.py` (ambang TMA + hujan)
- [ ] Catatan Sprint 2: cuplikan stdout pipeline

---

## Sprint 3 — Output & demo

**Eksekusi:** otomatis di `run_pipeline.sh`; verifikasi manual Langkah 5

- [ ] `output/output-1-level-siaga/alert_latest.json`
- [ ] `output/output-1-level-siaga/notifikasi_template.txt` dibaca tim
- [ ] `output/output-2-peta-terdampak/terdampak_latest.geojson` dibuka di Kepler.gl
- [ ] `output/output-3-logistik/logistik_ringkasan.pdf` dibuka
- [ ] `output/output-4-after-action/after_action_latest.md` dilengkapi tim
- [ ] Screenshot disimpan di `eksperimen/catatan/bukti/`
- [ ] [retrospective-sprint3.md](catatan/retrospective-sprint3.md) diisi
- [ ] Demo 5 menit untuk audiens non-teknis (rencana / terlaksana)

---

## Opsional — Kafka & MinIO

- [ ] `docker compose up` — container healthy
- [ ] `bash scripts/init_kafka.sh` — event terpublish
- [ ] `tma_siaga_stream.py --source kafka` berhasil
- [ ] MinIO bucket `banjir-musi` dibuat (`init_minio.sh`)

---

## Pengumpulan akhir

| Artefak | Lokasi |
|---|---|
| Log eksperimen | `eksperimen/catatan/log-eksperimen-*.md` |
| Bukti visual | `eksperimen/catatan/bukti/` |
| Retrospective | `eksperimen/catatan/retrospective-sprint3.md` |
| Checklist ini (terisi) | `eksperimen/catatan/checklist-terisi.md` (salinan opsional) |
