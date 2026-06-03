# Lampiran Praktikum — Studi Kasus Kebencanaan

Implementasi teknis tersedia di repositori (bukan hanya placeholder).

## Isi Lampiran

| Komponen | Lokasi |
|---|---|
| `docker-compose.yml` | `arsitektur-lab/` |
| Generator data sintetis | `data/scripts/` |
| Ingest Bronze/Silver | `analitik/batch/ingest_static.py` |
| Agregasi siaga TMA | `analitik/streaming/tma_siaga_stream.py` |
| Spatial join populasi | `analitik/batch/populasi_terdampak.py` |
| Routing shelter (KNN) | `analitik/batch/routing_evakuasi.py` |
| SQL Sedona (referensi) | `analitik/sql/` |
| Output 1–4 | `output/scripts/` |

## Menjalankan

```bash
cd arsitektur-lab && bash start.sh
```

Atau pipeline Python saja: lihat [arsitektur-lab/README.md](arsitektur-lab/README.md).

## Versi

| Versi | Tanggal | Catatan |
|---|---|---|
| 1.0 | 2026-05 | Kode lab lengkap + data sintetis |
