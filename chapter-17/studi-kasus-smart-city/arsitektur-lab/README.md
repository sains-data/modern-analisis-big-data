# Arsitektur Lab — Medan Smart City

Kafka **9097** · MinIO **9070/9071** · streaming-first (probe 15 dtk, IQU 10 mnt).

> [../eksperimen/README.md](../eksperimen/README.md)

```bash
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
```

| Komponen | Port |
|---|---|
| Kafka | 9097 |
| MinIO | 9070/9071 |
