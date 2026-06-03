# Instruksi — KEL Leuser

## Langkah 1 — Setup

```bash
cd sesi-praktikum/chapter-17/studi-kasus-konservasi/arsitektur-lab
chmod +x *.sh scripts/*.sh
cp .env.example .env   # opsional
```

## Langkah 2 — Data

```bash
bash scripts/prepare_data.sh
```

7 individu gajah · grid NDVI · patroli SMART · event edge.

## Langkah 3 — Pipeline

```bash
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
bash scripts/verify_stack.sh
```

## Langkah 4 — Verifikasi output

| Output | File |
|---|---|
| 1 Alert | `output/output-1-alert-konflik/pesan_whatsapp_sample.txt` |
| 2 Deforestasi | `output/output-2-bukti-deforestasi/deforestasi_latest.geojson` |
| 3 EUDR | `output/output-3-laporan-kel-eudr/laporan_kel_latest.pdf` |
| 4 Pergerakan | `output/output-4-basis-pergerakan/home_range_latest.geojson` |
| GPX patroli | `output/output-3-laporan-kel-eudr/rute_patroli_prioritas.gpx` |

## Langkah 5 — Demo Kepler

Import GeoJSON deforestasi + home range; jangan unggah layer GPS presisi.

## Pengumpulan

Log + bukti + retrospective di `eksperimen/catatan/`.
