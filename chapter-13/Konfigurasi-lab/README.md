# Konfigurasi Lab Chapter 13

Stack **monitoring infrastruktur Big Data**: Prometheus + Node Exporter + Grafana (sesuai Bab 13).

## Komponen

| Kontainer | Image | Port |
|---|---|---|
| `mon-prometheus` | prom/prometheus:v2.51.2 | 9090 |
| `mon-node-exporter` | prom/node-exporter:v1.7.0 | 9100 |
| `mon-grafana` | grafana/grafana:10.2.0 | 3000 |

## Struktur

```
Konfigurasi-lab/
├── docker-compose-monitoring.yml
├── prometheus/
│   ├── prometheus.yml
│   └── alert_rules.yml
├── grafana/provisioning/datasources/prometheus.yml
├── start.sh / stop.sh
└── scripts/
    ├── verify_stack.sh
    ├── promql_latihan.md
    ├── cpu_stress.sh
    ├── poll_cpu.sh
    ├── reload_prometheus.sh
    └── export_grafana_dashboard.sh
```

## Setup

```bash
cd sesi-praktikum/chapter-13/Konfigurasi-lab
chmod +x start.sh stop.sh scripts/*.sh
bash start.sh
sleep 30
bash scripts/verify_stack.sh
```

| UI | URL | Login |
|---|---|---|
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | admin / admin |
| Node Exporter | http://localhost:9100/metrics | — |

## Urutan latihan (tahap buku)

| Perintah / referensi | Tahap |
|---|---|
| `bash scripts/verify_stack.sh` | 1 |
| `scripts/promql_latihan.md` | 2 |
| Buat dashboard di Grafana (manual) | 3 |
| `bash scripts/cpu_stress.sh` + `poll_cpu.sh` | 4 |
| `reload_prometheus.sh`, `export_grafana_dashboard.sh` | 5 |

## Alert rules (default)

- `CPUUsageTinggi`, `MemoriKritis`, `DiskHampirPenuh`, `TargetDown`

Setelah edit `prometheus/alert_rules.yml`:

```bash
bash scripts/reload_prometheus.sh
```

## Catatan port

- **3000** Grafana — pastikan tidak bentrok layanan lain.
- **9090** Prometheus — jangan bentrok dengan Kafka UI modul lain jika memakai port sama.

## Hentikan

```bash
bash stop.sh
```
