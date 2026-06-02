# Chapter 4 — Ekosistem Hadoop

Praktik klaster Hadoop **pseudo-distributed** (HDFS, YARN, MapReduce WordCount) via Docker.

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

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | Build & start klaster, `jps` |
| [Latihan 2](Latihan2/README.md) | NameNode & YARN Web UI |
| [Latihan 3](Latihan3/README.md) | Operasi dasar HDFS |
| [Latihan 4](Latihan4/README.md) | MapReduce WordCount |
| [Latihan 5](Latihan5/README.md) | Manajemen HDFS & re-run job |
