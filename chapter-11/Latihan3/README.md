# Latihan 3 — Unsupervised Learning: K-Means Clustering
**Modul 9 · Machine Learning Big Data** | Estimasi waktu: **20 menit**

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Latihan 1–2 selesai

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Folder kerja | `Konfigurasi-lab/` |
| Script K-Means | `scripts/kmeans_elbow.py` |
| Input | `hdfs:///datalake/silver/transaksi/` |
| Output Gold | `hdfs:///datalake/gold/segmentasi_pelanggan/` |

## Langkah Kerja

### 1) Jalankan K-Means + elbow method

```bash
cd ../Konfigurasi-lab
bash scripts/spark_submit.sh /opt/modul9/scripts/kmeans_elbow.py
```

### 2) Catat hasil utama

- Nilai silhouette tiap K (2–7)
- Nilai inertia tiap K
- K terbaik
- Profil tiap cluster

### 3) Verifikasi output Gold layer

```bash
docker exec bigdata-spark hdfs dfs -ls /datalake/gold/segmentasi_pelanggan/
docker exec bigdata-spark hdfs dfs -du -h /datalake/gold/segmentasi_pelanggan/
```

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Pipeline ML End-to-End**.*
