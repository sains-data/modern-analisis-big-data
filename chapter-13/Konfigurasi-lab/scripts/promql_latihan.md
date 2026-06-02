# Query PromQL — Bab 13 Tahap 2

Jalankan di http://localhost:9090/graph (tab Graph & Table).

```promql
# 1. Daftar metrik node-exporter
{job="node-exporter"}

# 2. CPU usage rata-rata (%)
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# 3. Penggunaan memori (%)
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# 4. Disk usage per filesystem (%)
(node_filesystem_size_bytes{fstype!="tmpfs"} - node_filesystem_avail_bytes{fstype!="tmpfs"})
/ node_filesystem_size_bytes{fstype!="tmpfs"} * 100

# 5. Uptime (jam)
(node_time_seconds - node_boot_time_seconds) / 3600

# 6. Prediksi disk penuh (4 jam)
predict_linear(node_filesystem_avail_bytes{fstype!="tmpfs"}[1h], 4*3600) < 0

# 7. Load average
node_load1
node_load5
node_load15

# 8. Network receive (KB/s) — sesuaikan device jika bukan eth0
rate(node_network_receive_bytes_total{device!~"lo|docker.*"}[5m]) / 1024
```
