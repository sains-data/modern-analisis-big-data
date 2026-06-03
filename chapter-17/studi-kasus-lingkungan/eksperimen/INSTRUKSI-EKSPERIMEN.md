# Instruksi Eksperimen — Karhutla Riau

## Langkah 1 — `arsitektur-lab/`

```bash
cd sesi-praktikum/chapter-17/studi-kasus-lingkungan/arsitektur-lab
chmod +x *.sh scripts/*.sh
```

## Langkah 2 — Data sintetis

```bash
bash scripts/prepare_data.sh
```

Membuat: FIRMS VIIRS, konsesi, gambut, komponen H3, ISPU–ISPA.

## Langkah 3 — Pipeline

```bash
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
```

| Tahap | Output |
|---|---|
| Join akuntabilitas | `gold/hotspot_konsesi_agg.parquet` |
| Indeks risiko H3 | `gold/indeks_risiko_karhutla.parquet` |
| Korelasi | `gold/korelasi_ispu_ispa.parquet` |
| Emisi | `gold/emisi_karbon_konsesi.parquet` |

## Langkah 4 — Verifikasi & demo

```bash
bash scripts/verify_stack.sh
```

- Buka `output/output-1-peta-risiko/peta_risiko_latest.geojson` di Kepler.gl  
- Baca `output/output-2-akuntabilitas-konsesi/akuntabilitas_latest.pdf`  
- Bandingkan perusahaan `MELANGGAR` vs `MEMENUHI`

## Langkah 5 — Kafka (opsional)

```bash
docker compose up -d && bash scripts/init_kafka.sh
```

## Pengumpulan

`eksperimen/catatan/log-*.md`, `bukti/`, `retrospective-sprint3.md`
