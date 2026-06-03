# Analitik — Studi Kasus Kebencanaan

Pipeline **streaming** (TMA → siaga) dan **batch/geospasial** (genangan, populasi, routing).

## Struktur

```
analitik/
├── lib/                    # config, siaga, spatial
├── batch/
│   ├── ingest_static.py
│   ├── aggregate_tma.py
│   ├── populasi_terdampak.py
│   └── routing_evakuasi.py
├── streaming/
│   ├── tma_siaga_stream.py
│   └── kafka_producer_tma.py
├── sql/                    # referensi Sedona/Spark SQL
└── PANDUAN-ANALITIK.md
```

## Menjalankan (dari root studi kasus)

```bash
export PYTHONPATH="$(pwd)"
python analitik/batch/ingest_static.py
python analitik/streaming/tma_siaga_stream.py --source file
python analitik/batch/populasi_terdampak.py
```

Atau: `arsitektur-lab/scripts/run_pipeline.sh`

## Status

| Komponen | Status |
|---|---|
| Skrip Python lab | ✅ |
| PySpark cluster | Opsional (porting dari `sql/`) |

→ **[PANDUAN-ANALITIK.md](PANDUAN-ANALITIK.md)**
