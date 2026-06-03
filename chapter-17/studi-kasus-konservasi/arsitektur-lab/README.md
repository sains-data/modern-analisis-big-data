# Arsitektur Lab — KEL Leuser

Kafka **9096** · MinIO **9060/9061** · edge metadata + GPS streaming.

> [../eksperimen/README.md](../eksperimen/README.md)

```bash
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
```

| Komponen | Port |
|---|---|
| Kafka | 9096 |
| MinIO | 9060/9061 |
