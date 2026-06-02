# Latihan 1 — Menjalankan Klaster Hadoop
**Chapter 4 · Ekosistem Hadoop** | Estimasi waktu: **20 menit**

## Tujuan

- Menjalankan klaster Hadoop `pseudo-distributed`
- Memverifikasi daemon inti Hadoop aktif

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] File `hadoop-3.4.1.tar.gz` ada di `Konfigurasi-lab/vendor/bigdata-hadoop/`

## Langkah Kerja

```bash
cd ../Konfigurasi-lab
cp .env.example .env    # pertama kali
bash build.sh
bash start.sh
bash scripts/verify_cluster.sh
```

Opsional — shell interaktif:

```bash
bash login.sh
jps
```

## Output yang Diharapkan

`jps` menampilkan proses:
- `NameNode`
- `DataNode`
- `ResourceManager`
- `NodeManager`
- `SecondaryNameNode`

## Refleksi Singkat

1. Mengapa mode `pseudo-distributed` cukup untuk pembelajaran konsep Hadoop?
2. Apa dampak jika `NameNode` tidak aktif?

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — Eksplorasi Web UI Hadoop**.*
