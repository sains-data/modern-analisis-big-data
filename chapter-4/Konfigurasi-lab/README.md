# Konfigurasi Lab Chapter 4

Praktik chapter ini menjalankan klaster Hadoop **pseudo-distributed** berbasis Docker (repo [`sains-data/bigdata-hadoop`](https://github.com/sains-data/bigdata-hadoop)) untuk HDFS dan MapReduce.

Dataset teks **`latihan.txt`** dan **`dataset_wordcount.txt`** dihasilkan generator sintesis — kosakata selaras Bab 3+ (`partisipan`, `aktivitas`, `saluran`). Detail: [KATALOG-DATA.md](KATALOG-DATA.md).

## Referensi Lingkungan

| Item | Nilai |
|---|---|
| Repositori Hadoop | `vendor/bigdata-hadoop` (auto-clone) |
| Hadoop | `3.4.1` (tarball manual) |
| Kontainer | `bigdata-hadoop` |
| NameNode UI | http://localhost:9870 |
| ResourceManager UI | http://localhost:8088 |
| HDFS RPC | localhost:9000 |

## Struktur folder

```
Konfigurasi-lab/
├── build.sh / start.sh / login.sh / stop.sh
├── .env.example
├── KATALOG-DATA.md          ← isi teks & frekuensi WordCount harapan
├── data/
│   ├── latihan.txt          ← 7 kalimat (HDFS + kosakata platform)
│   └── dataset_wordcount.txt ← 6 baris token MapReduce
├── scripts/
│   ├── ensure_hadoop_repo.sh
│   ├── verify_cluster.sh
│   ├── hadoop_exec.sh
│   ├── copy_lab_data.sh
│   ├── setup_hdfs_latihan.sh
│   ├── prepare_wordcount_input.sh
│   ├── run_wordcount.sh
│   └── hdfs_management.sh
└── vendor/bigdata-hadoop/   ← hasil git clone (gitignored)
```

## Data latihan (ringkas)

| File | Isi |
|------|-----|
| `latihan.txt` | Narasi HDFS + pipeline medallion + partisipan/saluran/geografis |
| `dataset_wordcount.txt` | Token: partisipan, aktivitas, saluran, mobile, hadoop, hdfs, … |

Frekuensi kata tertinggi setelah WordCount: **`partisipan`** dan **`aktivitas`** (masing-masing 6×) — lihat tabel lengkap di KATALOG-DATA.

## 1) Prasyarat

- Docker aktif, RAM minimal 8 GB (disarankan 16 GB)
- `git`, `bash`
- Windows: WSL2 disarankan

## 2) Setup pertama kali

```bash
cd sesi-praktikum/chapter-4/Konfigurasi-lab
cp .env.example .env
chmod +x build.sh start.sh login.sh stop.sh scripts/*.sh

# Clone repo + cek tarball
bash scripts/ensure_hadoop_repo.sh
```

Unduh **`hadoop-3.4.1.tar.gz`** ke `vendor/bigdata-hadoop/`:

https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz

Pastikan file `.sh` di repo memakai line ending **LF**.

```bash
bash build.sh
bash start.sh
bash scripts/verify_cluster.sh
```

## 3) Skrip latihan (dari host)

| Skrip | Latihan | Fungsi |
|---|---|---|
| `scripts/setup_hdfs_latihan.sh` | 3 | Upload `latihan.txt`, fsck, report |
| `scripts/prepare_wordcount_input.sh` | 4 | Upload input WordCount |
| `scripts/run_wordcount.sh` | 4 | Job MapReduce WordCount |
| `scripts/hdfs_management.sh` | 5 | cp/mv/du, hapus output |
| `scripts/hdfs_management.sh --rerun-wordcount` | 5 | + jalankan ulang WordCount |

Atau shell interaktif di kontainer:

```bash
bash login.sh
# hdfs dfs ...
```

## 4) Path HDFS latihan

| Path | Isi |
|---|---|
| `/user/latihan/latihan.txt` | 7 kalimat teks latihan |
| `/user/latihan/input/dataset_wordcount.txt` | 6 baris input WordCount |
| `/user/latihan/output/part-r-00000` | Hasil reduce |
| `/user/latihan/arsip/` | Backup setelah latihan 5 |

## 5) Regenerasi data sintesis

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch04_hadoop
bash scripts/sync_to_chapters.sh
```

## 6) Hentikan klaster

```bash
bash stop.sh
```

## Troubleshooting

| Gejala | Solusi |
|---|---|
| File teks tidak ditemukan di kontainer | Pastikan `data/` terisi; jalankan sync dari `synthetic-data/` |
| WordCount frekuensi tidak sesuai | Regenerasi `ch04_hadoop`; pastikan input HDFS ter-overwrite (`prepare_wordcount_input.sh`) |
| Output directory already exists | `bash scripts/hdfs_management.sh` hapus output sebelum re-run |
