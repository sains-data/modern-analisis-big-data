# Chapter 5 — Apache Spark (PySpark)

Praktik PySpark pada klaster **Hadoop + Spark** (YARN): Monte Carlo π, DataFrame, Spark SQL, Parquet di HDFS.

## Alur cepat

```bash
cd sesi-praktikum/chapter-5/Konfigurasi-lab
cp .env.example .env
# unduh hadoop + spark tarball ke vendor/bigdata-spark/
bash build.sh && bash start.sh
bash scripts/setup_hdfs_mahasiswa.sh
bash scripts/run_hitung_pi.sh
bash scripts/run_analisis_nilai.sh
bash scripts/compare_hdfs_sizes.sh
bash stop.sh
```

Detail: **[Konfigurasi-lab/README.md](Konfigurasi-lab/README.md)**

## Latihan

| Latihan | Topik |
|---|---|
| [Latihan 1](Latihan1/README.md) | Setup klaster & data HDFS |
| [Latihan 2](Latihan2/README.md) | `hitung_pi.py` — RDD Monte Carlo |
| [Latihan 3](Latihan3/README.md) | `analisis_nilai.py` — DataFrame & SQL |
| [Latihan 4](Latihan4/README.md) | Spark UI, YARN UI, ukuran file |
| [Latihan 5](Latihan5/README.md) | Partisi & cache RDD |
