# Latihan 3 — Dashboard Grafana
**Chapter 13 · Monitoring Infrastruktur Big Data** | Estimasi: **35 menit** | **Tahap 3**

## Tujuan

- Memverifikasi datasource **Prometheus**
- Membangun dashboard **`BigData Infrastructure Monitoring`** (4 panel)

## Prasyarat

- [ ] Latihan 1–2 selesai

## Langkah kerja

### 3.1 Datasource

1. Login http://localhost:3000 (`admin` / `admin`)
2. **Connections → Data Sources → Prometheus → Save & Test**  
   Harus: *Data source is working*

### 3.2 Dashboard baru

**Dashboards → New → New Dashboard → Add visualization**

### 3.3 Panel — CPU Gauge

```promql
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

- Visualization: **Gauge**  
- Title: `CPU Usage (%)`  
- Unit: percent (0–100)  
- Thresholds: 0–60 hijau, 60–80 kuning, 80–100 merah  

### 3.4 Panel — Memory Gauge

```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

- Title: `Memory Usage (%)` — threshold sama  

### 3.5 Panel — CPU Time Series

```promql
rate(node_cpu_seconds_total[5m]) * 100
```

- Title: `CPU Usage per Mode`  
- Legend: `{{mode}}`  

### 3.6 Panel — Load Average

Tiga query: `node_load1`, `node_load5`, `node_load15` (legend: 1m, 5m, 15m)  
- Title: `System Load Average`  

### 3.7 Layout & simpan

```
┌────────────────────┬────────────────────┐
│ CPU Usage (%)      │ Memory Usage (%)   │
├────────────────────┴────────────────────┤
│ CPU Usage per Mode (time series)        │
├─────────────────────────────────────────┤
│ System Load Average                     │
└─────────────────────────────────────────┘
```

**Save Dashboard** → nama: `BigData Infrastructure Monitoring`

## Checklist

| Panel | Selesai |
|---|---|
| CPU Gauge | |
| Memory Gauge | |
| CPU per Mode | |
| Load Average | |

---

*Latihan 3 selesai. Lanjut **Latihan 4 — Alert & Beban**.*
