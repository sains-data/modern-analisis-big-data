# Instruksi — Kota Medan

## Langkah 1 — Setup

```bash
cd sesi-praktikum/chapter-17/studi-kasus-smart-city/arsitektur-lab
chmod +x *.sh scripts/*.sh
```

## Langkah 2 — Data

```bash
bash scripts/prepare_data.sh
```

25 ruas · 15 sensor udara · probe vehicle · GTFS TMD.

## Langkah 3 — Pipeline

```bash
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
bash scripts/verify_stack.sh
```

## Langkah 4 — Verifikasi output

| Output | File |
|---|---|
| 1 ATCS | `output/output-1-atcs/kondisi_jalan_latest.geojson` |
| 2 IQU | `output/output-2-iqu-hiperlokal/iqu_grid_latest.geojson` |
| 3 TMD | `output/output-3-optimasi-tmd/rekomendasi_tmd_latest.pdf` |
| 4 Emisi | `output/output-4-laporan-emisi/emisi_kecamatan_latest.pdf` |

## Langkah 5 — Demo Kepler

Import GeoJSON ATCS + IQU; filter kecamatan untuk Sprint Review.

## Pengumpulan

Log + bukti + jawaban 2 pertanyaan klien di `eksperimen/catatan/`.
