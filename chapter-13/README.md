# Chapter 13 — Monitoring Infrastruktur Big Data

Praktik **Prometheus + Node Exporter + Grafana**: PromQL, dashboard, alert rules, uji beban CPU.

## Alur cepat

```bash
cd sesi-praktikum/chapter-13/Konfigurasi-lab
bash start.sh
bash scripts/verify_stack.sh
# Latihan 2: promql di http://localhost:9090/graph
# Latihan 3–4: Grafana http://localhost:3000
bash scripts/cpu_stress.sh 2 60
bash stop.sh
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan ↔ Tahap buku

| Latihan | Tahap | Topik |
|---|---|---|
| [Latihan 1](Latihan1/README.md) | 1 | Stack `mon-*`, verifikasi target |
| [Latihan 2](Latihan2/README.md) | 2 | PromQL di Expression Browser |
| [Latihan 3](Latihan3/README.md) | 3 | Dashboard `BigData Infrastructure Monitoring` |
| [Latihan 4](Latihan4/README.md) | 4 | Alert rules + beban CPU |
| [Latihan 5](Latihan5/README.md) | 5 | Disk panel, alert tambahan, ekspor JSON |
