# Analitik — Stunting Sumatera Utara

```
analitik/
├── lib/          config, who_lms, alert, indeks
├── batch/        ingest, zscore, prevalensi, akses, indeks, DBSCAN
├── streaming/    alert_kader_stream, kafka_producer_upload
└── sql/          zscore_prevalensi_desa.sql
```

```bash
export PYTHONPATH="$(cd .. && pwd)"
# atau: arsitektur-lab/scripts/run_pipeline.sh
```

| Skrip buku | Implementasi lab |
|---|---|
| `output_01_prioritas_desa.py` | `output/scripts/output_01_prioritas_desa.py` |
| `output_02_dashboard_tpps.py` | `output/scripts/output_02_dashboard_tpps.py` |
| `output_03_alert_kader.py` | `analitik/streaming/alert_kader_stream.py` |

→ [PANDUAN-ANALITIK.md](PANDUAN-ANALITIK.md)
