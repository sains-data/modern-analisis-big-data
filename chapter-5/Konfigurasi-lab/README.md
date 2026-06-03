# Konfigurasi Lab Chapter 5

Praktik **PySpark pada YARN** dengan klaster Hadoop + Spark (`bigdata-spark`, Docker).

Dataset **`mahasiswa.csv`** (10 baris) berasal dari entitas sintesis **`skor_kompetensi`** — kosakata dan nama partisipan selaras Bab 3+. Detail: [KATALOG-DATA.md](KATALOG-DATA.md).

## Referensi Lingkungan

| Item | Nilai |
|---|---|
| Repo | `vendor/bigdata-spark` (auto-clone) |
| Hadoop / Spark | 3.4.1 / 3.5.5 (tarball manual) |
| Kontainer | `bigdata-spark` |
| Path HDFS | `/user/lab/modul5` (default, lihat `.env`) |
| Skrip di kontainer | `/opt/spark-jobs/` |
| NameNode UI | http://localhost:9870 |
| YARN UI | http://localhost:8088 |
| Spark UI | http://localhost:4040 |

## Struktur folder

```
Konfigurasi-lab/
├── build.sh / start.sh / login.sh / stop.sh
├── KATALOG-DATA.md          ← schema & mapping skor kompetensi
├── app/
│   ├── hitung_pi.py
│   ├── hitung_pi_cache.py
│   └── analisis_nilai.py
├── data/
│   ├── mahasiswa.csv        ← 10 baris (format legacy lab)
│   └── skor_kompetensi.csv  ← 10 baris (schema kanonik)
└── scripts/
    ├── ensure_spark_repo.sh
    ├── verify_cluster.sh
    ├── setup_hdfs_mahasiswa.sh
    ├── run_hitung_pi.sh
    ├── run_analisis_nilai.sh
    ├── run_hitung_pi_cache.sh
    └── compare_hdfs_sizes.sh
```

## Data latihan (ringkas)

| Kolom legacy | Kolom kanonik | Keterangan |
|--------------|---------------|------------|
| `nim` | `id_partisipan` | Alias `2021001` = `PK-0001` |
| `nilai_uts` | `skor_modul_a` | Modul fintech |
| `nilai_uas` | `skor_modul_b` | Modul operasional |
| `nilai_tugas` | `skor_modul_c` | Modul analitik data |

Distribusi grade setelah `analisis_nilai.py`: A=1, B=2, C=3, D=3, E=1.

## Setup pertama kali

```bash
cd sesi-praktikum/chapter-5/Konfigurasi-lab
cp .env.example .env
chmod +x *.sh scripts/*.sh
bash scripts/ensure_spark_repo.sh
```

Unduh ke `vendor/bigdata-spark/`:
- [hadoop-3.4.1.tar.gz](https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz)
- [spark-3.5.5-bin-hadoop3.tgz](https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz)

```bash
bash build.sh
bash start.sh
bash scripts/setup_hdfs_mahasiswa.sh
```

## Urutan latihan (dari host)

| Perintah | Latihan |
|---|---|
| `bash scripts/verify_cluster.sh` | 1 |
| `bash scripts/run_hitung_pi.sh` | 2 |
| `bash scripts/run_analisis_nilai.sh` | 3 |
| `bash scripts/compare_hdfs_sizes.sh` | 4 |
| `SLICES=8 bash scripts/run_hitung_pi.sh` | 5A |
| `bash scripts/run_hitung_pi_cache.sh` | 5B |

## Regenerasi data sintesis

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch05_spark
bash scripts/sync_to_chapters.sh
```

## Hentikan klaster

```bash
bash stop.sh
```

## Troubleshooting

| Gejala | Solusi |
|---|---|
| `mahasiswa.csv` tidak ditemukan | Sync dari `synthetic-data/`; cek `data/` |
| Grade tidak sesuai harapan | Pastikan CSV belum diubah manual; regenerasi `ch05_spark` |
| HDFS upload gagal | `bash scripts/copy_spark_jobs.sh` lalu `setup_hdfs_mahasiswa.sh` |
