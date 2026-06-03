# Chapter 4 — Ekosistem Hadoop

Praktik klaster Hadoop **pseudo-distributed** (HDFS, YARN, MapReduce WordCount) via Docker.

Dataset teks latihan (`latihan.txt`, `dataset_wordcount.txt`) dihasilkan generator sintesis [`synthetic-data/`](../../synthetic-data/README.md) dengan kosakata selaras entitas platform partisipan (Bab 3+).

## Alur cepat

```bash
cd sesi-praktikum/chapter-4/Konfigurasi-lab
cp .env.example .env
# unduh hadoop-3.4.1.tar.gz ke vendor/bigdata-hadoop/
bash build.sh && bash start.sh
bash scripts/verify_cluster.sh
bash scripts/setup_hdfs_latihan.sh
bash scripts/prepare_wordcount_input.sh
bash scripts/run_wordcount.sh
bash scripts/hdfs_management.sh --rerun-wordcount
bash stop.sh
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)** · **[KATALOG-DATA.md](Konfigurasi-lab/KATALOG-DATA.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | Build & start klaster, `jps` |
| [Latihan 2](Latihan2/README.md) | NameNode & YARN Web UI |
| [Latihan 3](Latihan3/README.md) | Operasi dasar HDFS |
| [Latihan 4](Latihan4/README.md) | MapReduce WordCount |
| [Latihan 5](Latihan5/README.md) | Manajemen HDFS & re-run job |

## Data latihan

| File | Volume | Fungsi |
|------|--------|--------|
| `data/latihan.txt` | 7 kalimat | Upload HDFS, fsck (Latihan 3) |
| `data/dataset_wordcount.txt` | 6 baris token | Input MapReduce (Latihan 4–5) |

Kosakata dominan WordCount: `partisipan`, `aktivitas`, `saluran`, `mobile`, `hadoop`, `hdfs`.

## File eksekusi (di `Konfigurasi-lab/`)

| Path | Fungsi |
|---|---|
| `data/latihan.txt` | Teks latihan HDFS |
| `data/dataset_wordcount.txt` | Input WordCount |
| `KATALOG-DATA.md` | Schema teks & frekuensi harapan |
| `scripts/setup_hdfs_latihan.sh` | Upload latihan.txt |
| `scripts/prepare_wordcount_input.sh` | Upload input WordCount |
| `scripts/run_wordcount.sh` | Job MapReduce |
| `scripts/hdfs_management.sh` | Manajemen & re-run |
