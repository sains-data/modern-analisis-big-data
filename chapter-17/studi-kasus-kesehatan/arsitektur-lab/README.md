# Arsitektur Lab — Stunting Sumatera Utara

Kafka **9094** · MinIO **9040/9041** · pipeline Python (z-score WHO, indeks 5 dimensi, alert streaming).

> Panduan praktikum: [../eksperimen/README.md](../eksperimen/README.md)  
> **Eksekusi kode di folder ini.**

```bash
chmod +x *.sh scripts/*.sh
bash scripts/prepare_data.sh
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
```

Atau: `bash start.sh` (termasuk Docker jika tersedia).

## Port

| Layanan | Port |
|---|---|
| Kafka | 9094 |
| MinIO | 9040 / 9041 |

## Catatan lab

- Aksesibilitas memakai **haversine** (bukan OSRM penuh); produksi: build graph OSM Sumut.  
- LMS WHO disederhanakan untuk latihan — validasi konsep, bukan replika tabel resmi.
