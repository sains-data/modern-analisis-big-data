# Sesi Praktikum — Analisis Big Data: Teori dan Praktik

Repositori ini berisi **kode, konfigurasi lab, dataset contoh, dan panduan latihan** untuk mata kuliah **Analisis Big Data** di Program Studi Sains Data, Institut Teknologi Sumatera (ITERA). Materi praktikum menyertai buku *Modern Analisis Big Data: Teori dan Praktik* (Ardika Satria · Luluk Muthoharoh · Febri Dwi Irawati).

Pembaca diasumsikan sudah memahami **Python**, **basis data relasional**, dan penggunaan dasar **Linux**. Setiap bab praktikum membangun kompetensi sebelumnya: dari arsitektur dan Hadoop, pemrosesan Spark, penyimpanan lakehouse, streaming dan ML, hingga analitik spasial dan studi kasus terapan di Sumatera.

---

## Repositori GitHub resmi

Seluruh kode praktikum, skrip konfigurasi lingkungan (Docker, Hadoop, Spark, Kafka, MinIO), dataset contoh, dan pembaruan mengikuti versi teknologi terkini tersedia secara terbuka:

| Repositori | Peran |
|---|---|
| **[github.com/sains-data/praktikum-analisis-big-data](https://github.com/sains-data/praktikum-analisis-big-data)** | **Praktikum** — folder `sesi-praktikum/` (repositori ini) |
| **[github.com/sains-data/modern-analisis-big-data](https://github.com/sains-data/modern-analisis-big-data)** | **Buku** — sumber LaTeX, teori Bab 1–17, diagram, dan rujukan konsep |

Clone praktikum:

```bash
git clone https://github.com/sains-data/praktikum-analisis-big-data.git
cd praktikum-analisis-big-data/sesi-praktikum
```

Disarankan memberi **star** pada kedua repositori agar mendapat notifikasi pembaruan modul dan kompatibilitas versi stack.

---

## Peta buku dan praktikum

Buku dibagi **tujuh bagian** (Bab 1–17). Folder `chapter-N/` di repositori ini selaras dengan **bab praktikum** di buku, bukan dengan nomor modul LMS secara otomatis.

### Bagian I — Fundamental Big Data (Bab 1–2)

| Bab | Topik (buku) | Folder praktikum |
|---|---|---|
| **1** | Lanskap big data, transformasi digital, relevansi industri | — *(materi teori; tidak ada lab terpisah di repo ini)* |
| **2** | Karakteristik **5V**, sumber data, siklus hidup data | — *(materi teori; tidak ada lab terpisah di repo ini)* |

Bab 1–2 menjadi fondasi konsep sebelum masuk lab. Rujukan lengkap ada di repositori buku [`modern-analisis-big-data`](https://github.com/sains-data/modern-analisis-big-data).

### Bagian II — Arsitektur dan Ekosistem (Bab 3–4)

| Bab | Topik | Folder |
|---|---|---|
| **3** | Lambda/Kappa, **medallion** Bronze–Silver–Gold, data lake/lakehouse | [chapter-3](chapter-3/README.md) |
| **4** | **Hadoop**: HDFS, MapReduce, YARN | [chapter-4](chapter-4/README.md) |

### Bagian III — Pemrosesan Data Skala Besar (Bab 5–7)

| Bab | Topik | Folder |
|---|---|---|
| **5** | **Apache Spark**: RDD, DataFrame, eksekusi terdistribusi | [chapter-5](chapter-5/README.md) |
| **6** | Spark SQL, Catalyst, join, partisi, optimasi | [chapter-6](chapter-6/README.md) |
| **7** | **Apache Arrow**, PyArrow, DuckDB, Polars | [chapter-7](chapter-7/README.md) |

### Bagian IV — Penyimpanan dan Tata Kelola (Bab 8–9)

| Bab | Topik | Folder |
|---|---|---|
| **8** | Hive, HBase, Parquet/ORC, **Iceberg**, pipeline medallion | [chapter-8](chapter-8/README.md) |
| **9** | **Airflow**, kualitas data, lineage, metadata | [chapter-9](chapter-9/README.md) |

### Bagian V — Analitik Kecerdasan Big Data (Bab 10–13)

| Bab | Topik | Folder |
|---|---|---|
| **10** | **Kafka**, windowing, Spark Structured Streaming | [chapter-10](chapter-10/README.md) |
| **11** | **MLlib**, feature engineering, ML terdistribusi | [chapter-11](chapter-11/README.md) |
| **12** | Visualisasi, **Superset**, eksplorasi SQL | [chapter-12](chapter-12/README.md) |
| **13** | **Prometheus**, **Grafana**, monitoring infrastruktur | [chapter-13](chapter-13/README.md) |

### Bagian VI — Pengembangan dan Produksi (Bab 14–15)

| Bab | Topik | Folder |
|---|---|---|
| **14** | Studi kasus terpadu: Trino, e-commerce, fintech, evaluasi dashboard | [chapter-14](chapter-14/README.md) |
| **15** | Debugging, RCA, ELK, Jaeger, observability | — *(tidak ada sesi praktikum terpisah; lanjut Bab 16)* |

### Bagian VII — Spasial dan Studi Kasus Sumatera (Bab 16–17)

| Bab | Topik | Folder |
|---|---|---|
| **16** | **Apache Sedona**, H3, GeoParquet, Moran’s I, Gi*, DBSCAN | [chapter-16](chapter-16/README.md) |
| **17** | Enam studi kasus PBL + Scrum (multimodal, Sumatera) | [chapter-17](chapter-17/README.md) |

#### Studi kasus Bab 17 (kode lab lengkap)

| Studi kasus | Domain | Mulai di |
|---|---|---|
| [studi-kasus-kebencanaan](chapter-17/studi-kasus-kebencanaan/eksperimen/README.md) | Peringatan dini banjir DAS Musi | `eksperimen/` → `arsitektur-lab/` |
| [studi-kasus-lingkungan](chapter-17/studi-kasus-lingkungan/eksperimen/README.md) | Karhutla & gambut Riau | sama |
| [studi-kasus-kesehatan](chapter-17/studi-kasus-kesehatan/eksperimen/README.md) | Stunting Sumatera Utara | sama |
| [studi-kasus-konservasi](chapter-17/studi-kasus-konservasi/eksperimen/README.md) | KEL Leuser | sama |
| [studi-kasus-smart-city](chapter-17/studi-kasus-smart-city/eksperimen/README.md) | ATCS & IQU Medan | sama |
| [studi-kasus-edukasi](chapter-17/studi-kasus-edukasi/eksperimen/README.md) | Big data akademik PT | sama |

---

## Keselarasan 10 modul praktikum (mata kuliah)

Daftar modul di [Kata Pengantar](preface.tex) (`preface.tex`) dan jadwal kelas:

| Modul | Judul (singkat) | Bab / folder utama |
|---|---|---|
| 1 | Desain arsitektur & platform | [chapter-3](chapter-3/README.md) |
| 2 | Ekosistem Hadoop | [chapter-4](chapter-4/README.md) |
| 3 | Pemrosesan big data (1) | [chapter-5](chapter-5/README.md) |
| 4 | Pemrosesan big data (2) | [chapter-6](chapter-6/README.md) |
| 5 | Pemrosesan big data (3) | [chapter-7](chapter-7/README.md) |
| 6 | Struktur & penyimpanan | [chapter-8](chapter-8/README.md) |
| 7 | Orkestrasi & tata kelola | [chapter-9](chapter-9/README.md) |
| 8 | Analitik aliran data | [chapter-10](chapter-10/README.md) |
| 9 | Machine learning big data | [chapter-11](chapter-11/README.md) |
| 10 | Monitoring, visualisasi, eksplorasi | [chapter-12](chapter-12/README.md) · [chapter-13](chapter-13/README.md) · [chapter-14](chapter-14/README.md) |

Modul 10 di kelas dapat dibagi beberapa pertemuan; Bab 16–17 biasanya pertemuan akhir atau proyek integratif.

---

## Struktur folder per bab (Bab 3–16)

Pola umum:

```
chapter-N/
├── README.md              # Ringkasan bab & alur cepat
├── Konfigurasi-lab/       # docker-compose, start.sh, skrip utama
├── Latihan1/ … Latihan5/  # Instruksi per sesi (120 menit)
└── Data/                  # Dataset contoh (jika ada)
```

**Bab 17** memakai pola proyek:

```
chapter-17/studi-kasus-<domain>/
├── eksperimen/            # Mulai praktikum di sini
├── arsitektur-lab/        # Docker, pipeline, .venv
├── data/                  # Bronze / Silver / Gold
├── analitik/              # Batch & streaming
└── output/                # Deliverable ke pemangku kebijakan
```

---

## Cara memulai

1. **Clone** repositori praktikum (lihat tautan GitHub di atas).
2. Baca **README** bab yang sedang dikerjakan (mis. [chapter-3](chapter-3/README.md)).
3. Masuk ke **`Konfigurasi-lab/`** (atau `arsitektur-lab/` untuk Bab 17), ikuti `start.sh` / panduan di README bab.
4. Kerjakan **Latihan 1–5** sesuai urutan; kumpulkan laporan sesuai ketentuan kelas (LMS / repositori yang ditetapkan dosen).

Contoh Bab 3 (Data Lake + MinIO):

```bash
cd chapter-3/Konfigurasi-lab
bash start.sh
docker exec -it bigdata-compute python upload_bronze.py
docker exec -it bigdata-compute python transform.py
docker exec -it bigdata-compute python aggregate.py
docker exec -it bigdata-compute python verify_pipeline.py
```

Contoh Bab 17 (studi kasus):

```bash
cd chapter-17/studi-kasus-kebencanaan/arsitektur-lab
chmod +x *.sh scripts/*.sh
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/prepare_data.sh && bash scripts/run_pipeline.sh
```

---

## Prasyarat lingkungan

| Kebutuhan | Catatan |
|---|---|
| **Git** | Clone & update repo |
| **Docker** & **Docker Compose** | Mayoritas lab Bab 3–16 |
| **Python 3.10+** | PySpark, skrip Bab 17, producer Kafka |
| **RAM 8 GB+** | Disarankan 16 GB untuk Spark + Kafka bersamaan |
| **Linux / macOS / WSL2** | Perintah bash di panduan mengasumsikan shell Unix |

Beberapa bab memakai klaster Hadoop/Spark eksternal (repo [`sains-data/bigdata-hadoop`](https://github.com/sains-data/bigdata-hadoop), [`sains-data/bigdata-spark`](https://github.com/sains-data/bigdata-spark)) — detail ada di README masing-masing bab.

---

## Panduan pelaksanaan (ringkas)

Ketentuan resmi praktikum (asisten, praktikan, penilaian, alur 120 menit) tercantum lengkap di **[preface.tex](preface.tex)** — bagian *Panduan Pelaksanaan Praktikum*.

**Nilai akhir praktikum (ringkas):**

- Pre-Test **10%**
- Tugas Lab **45%**
- Take Home **45%**

**Alur satu pertemuan:** Pre-Test (10 mnt) → penjelasan asisten (≤10 mnt) → tugas lab (90 mnt) → pengarahan take-home (10 mnt); laporan individu **H+3**.

---

## Kontribusi dan pembaruan

Ekosistem big data berubah cepat (Iceberg, lakehouse, streaming, observability). Issue dan pull request pada [praktikum-analisis-big-data](https://github.com/sains-data/praktikum-analisis-big-data) dipersilakan untuk perbaikan instruksi, versi image Docker, dan kompatibilitas dependensi — dengan merujuk bab dan versi tool yang digunakan.

---

## Penulis

**Ardika Satria** · **Luluk Muthoharoh** · **Febri Dwi Irawati**  
Program Studi Sains Data, Institut Teknologi Sumatera (ITERA) · Lampung Selatan, 2026

Kata pengantar lengkap: [preface.tex](preface.tex).
