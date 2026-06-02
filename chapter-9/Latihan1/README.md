# Latihan 1 — Membuat DAG Airflow Sederhana
**Chapter 9 · Orkestrasi dan Tata Kelola Data** | Estimasi waktu: **20 menit**

---

## Tujuan Latihan

Setelah menyelesaikan latihan ini, mahasiswa mampu:
- Mendefinisikan DAG Airflow menggunakan Python dengan `BashOperator` dan `PythonOperator`
- Memahami konsep dependensi antar-task menggunakan operator `>>`
- Menggunakan XCom untuk mengirim nilai dari satu task ke task lain
- Mengaktifkan dan memonitor DAG melalui Airflow Web UI (Graph, Grid, Log)
- Membaca log eksekusi setiap task untuk memverifikasi keberhasilan

---

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Kontainer `bigdata-spark` berjalan (`docker ps | grep bigdata-spark`)
- [ ] Stack Airflow/Atlas aktif (`docker ps | grep modul7-airflow`)
- [ ] Airflow UI dapat diakses di `http://localhost:18681` (login: `airflow / airflow`)
- [ ] `bash scripts/setup_bigdata_spark.sh` sudah dijalankan
- [ ] Direktori `Konfigurasi-lab/dags/` sudah ada

---

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Airflow UI | http://localhost:18681 (`airflow` / `airflow`) |
| CLI Airflow | `docker exec modul7-airflow-scheduler airflow ...` |
| Perintah HDFS/Spark | `docker exec bigdata-spark ...` |
| Path DAG | `Konfigurasi-lab/dags/latihan_pipeline.py` |
| Generator data | `/opt/scripts/generate_data.py` (di dalam `bigdata-spark`) |

---

## Langkah Kerja

### Langkah 1.1 — Verifikasi Airflow berjalan

Dari terminal **host** (WSL/Linux):

```bash
# Cek container Airflow
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep modul7-airflow

# Cek health webserver
curl -s http://localhost:18681/health
```

Jika webserver tidak berjalan, dari folder `Konfigurasi-lab/`:

```bash
bash start.sh
```

---

### Langkah 1.2 — Buat file DAG

```bash
nano Konfigurasi-lab/dags/latihan_pipeline.py
```

Salin kode berikut secara lengkap:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import subprocess

BIGDATA = "/opt/airflow/scripts/bigdata_exec.sh"

default_args = {
    "owner": "mahasiswa",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def validasi_data(**context):
    """Cek file CSV di bigdata-spark (/tmp) via docker exec."""
    tanggal = context["ds_nodash"]
    cmd = (
        f"test -f /tmp/transaksi_{tanggal}.csv && "
        f"wc -l < /tmp/transaksi_{tanggal}.csv"
    )
    result = subprocess.run(
        ["docker", "exec", "bigdata-spark", "bash", "-lc", cmd],
        capture_output=True,
        text=True,
        check=True,
    )
    jumlah = int(result.stdout.strip()) - 1  # minus header
    print(f"[VALIDASI] Ditemukan {jumlah} baris data.")
    context["ti"].xcom_push(key="jumlah_baris", value=jumlah)


def cetak_laporan(**context):
    jumlah = context["ti"].xcom_pull(
        task_ids="validasi_data",
        key="jumlah_baris",
    )
    print(f"[LAPORAN] Pipeline selesai. Total baris: {jumlah}")


with DAG(
    dag_id="latihan_pipeline_transaksi",
    default_args=default_args,
    description="DAG latihan chapter 9 - pipeline sederhana",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["latihan", "chapter9"],
) as dag:

    mulai = EmptyOperator(task_id="mulai")

    buat_file = BashOperator(
        task_id="buat_file_simulasi",
        bash_command=(
            f"{BIGDATA} "
            "'python /opt/scripts/generate_data.py {{ ds }} 100 "
            "> /tmp/transaksi_{{ ds_nodash }}.csv && "
            "echo File berhasil dibuat: $(wc -l < /tmp/transaksi_{{ ds_nodash }}.csv) baris'"
        ),
    )

    validasi = PythonOperator(
        task_id="validasi_data",
        python_callable=validasi_data,
    )

    ingest_hdfs = BashOperator(
        task_id="ingest_ke_hdfs",
        bash_command=(
            f"{BIGDATA} "
            "'hdfs dfs -mkdir -p /datalake/bronze/latihan/ && "
            "hdfs dfs -put -f /tmp/transaksi_{{ ds_nodash }}.csv "
            "/datalake/bronze/latihan/ && "
            "hdfs dfs -ls /datalake/bronze/latihan/'"
        ),
    )

    laporan = PythonOperator(
        task_id="cetak_laporan",
        python_callable=cetak_laporan,
    )

    selesai = EmptyOperator(task_id="selesai")

    mulai >> buat_file >> validasi >> ingest_hdfs >> laporan >> selesai
```

Simpan: `Ctrl+O` → `Enter` → `Ctrl+X`

> **Catatan:** Task Bash memanggil `bigdata_exec.sh` agar perintah HDFS/Python dijalankan di kontainer `bigdata-spark`, sementara Airflow scheduler tetap di stack Docker Chapter 9.

---

### Langkah 1.3 — Verifikasi DAG terdeteksi oleh scheduler

```bash
sleep 15
docker exec modul7-airflow-scheduler airflow dags list | grep latihan_pipeline_transaksi
```

Jika tidak muncul, cek syntax:

```bash
python3 Konfigurasi-lab/dags/latihan_pipeline.py
```

---

### Langkah 1.4 — Trigger DAG secara manual

```bash
docker exec modul7-airflow-scheduler airflow dags trigger latihan_pipeline_transaksi
sleep 5
docker exec modul7-airflow-scheduler airflow dags list-runs latihan_pipeline_transaksi
```

Catat **run_id** pada **Tabel 1.1**.

---

### Langkah 1.5 — Pantau status task via CLI

```bash
RUN_ID=$(docker exec modul7-airflow-scheduler airflow dags list-runs \
  latihan_pipeline_transaksi --output json 2>/dev/null \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d[0]['run_id'])")

echo "Run ID: $RUN_ID"

watch -n 15 "docker exec modul7-airflow-scheduler airflow tasks states-for-dag-run \
  latihan_pipeline_transaksi '$RUN_ID'"
```

Tekan `Ctrl+C` setelah semua task berstatus `success`. Catat pada **Tabel 1.2**.

---

### Langkah 1.6 — Baca log setiap task

```bash
docker exec modul7-airflow-scheduler airflow tasks logs \
  latihan_pipeline_transaksi buat_file_simulasi "$RUN_ID" 1

docker exec modul7-airflow-scheduler airflow tasks logs \
  latihan_pipeline_transaksi validasi_data "$RUN_ID" 1

docker exec modul7-airflow-scheduler airflow tasks logs \
  latihan_pipeline_transaksi cetak_laporan "$RUN_ID" 1
```

Catat output penting pada **Tabel 1.2**.

---

### Langkah 1.7 — Verifikasi melalui Airflow Web UI

Buka `http://localhost:18681`. Login dengan `airflow / airflow`.

Di halaman **DAGs**, cari `latihan_pipeline_transaksi` dan klik namanya.

**Amati tab Graph, Grid, Log, dan XCom** — catat pada **Tabel 1.3**.

---

### Langkah 1.8 — Verifikasi file di HDFS

```bash
docker exec bigdata-spark hdfs dfs -ls /datalake/bronze/latihan/
docker exec bigdata-spark bash -lc \
  'hdfs dfs -cat /datalake/bronze/latihan/transaksi_$(date +%Y%m%d).csv | head -5'
```

Catat path dan isi file pada **Tabel 1.1**.

---

## Tabel Pencatatan Hasil

### Tabel 1.1 — Informasi Eksekusi DAG

| Informasi | Nilai yang Tercatat |
|---|---|
| Run ID DAG | _..._ |
| Tanggal eksekusi (`ds`) | _..._ |
| Nama file CSV yang dibuat | `/tmp/transaksi_` _..._ `.csv` (di bigdata-spark) |
| Jumlah baris di file CSV (termasuk header) | _..._ |
| Path HDFS tempat file disimpan | _..._ |
| Apakah file CSV terlihat di HDFS? | Ya / Tidak |

### Tabel 1.2 — Status dan Durasi Setiap Task

| Task | Status Akhir | Durasi (detik) | Pesan Penting dari Log |
|---|---|---|---|
| `mulai` | _success/failed_ | _..._ | _(EmptyOperator)_ |
| `buat_file_simulasi` | _..._ | _..._ | _..._ |
| `validasi_data` | _..._ | _..._ | `[VALIDASI] Ditemukan ... baris` |
| `ingest_ke_hdfs` | _..._ | _..._ | _..._ |
| `cetak_laporan` | _..._ | _..._ | `[LAPORAN] Pipeline selesai. Total baris: ...` |
| `selesai` | _..._ | _..._ | _(EmptyOperator)_ |
| **Total durasi pipeline** | — | **_..._ detik** | — |

### Tabel 1.3 — Pengamatan Airflow Web UI

| Aspek yang Diamati | Hasil |
|---|---|
| Jumlah node di tab Graph | _..._ |
| Bentuk alur (linear / bercabang / gabungan) | _..._ |
| Warna semua node setelah eksekusi | _..._ |
| Jumlah baris yang tervalidasi (dari log validasi_data) | _..._ |
| Nilai XCom `jumlah_baris` yang diterima task laporan | _..._ |
| Apakah nilai XCom sama dengan jumlah baris validasi? | Ya / Tidak |
| Task dengan durasi terpanjang | _..._ (_..._ detik) |
| Task dengan durasi terpendek | _..._ (_..._ detik) |

### Tabel 1.4 — Analisis Struktur DAG

```
mulai → ___ → ___ → ___ → ___ → selesai
```

---

## Refleksi dan Analisis

**R1.1 — DAG menggunakan `EmptyOperator` untuk task `mulai` dan `selesai` meskipun keduanya tidak melakukan komputasi apapun. Dari perspektif desain pipeline, apa fungsi arsitektural dari task-task ini? Berikan satu skenario konkret di mana task `mulai` bisa diisi dengan sesuatu yang lebih berguna.**

> Tulis jawaban Anda di sini:
>
> _..._

---

**R1.2 — Dari Tabel 1.2, task `ingest_ke_hdfs` menggunakan `BashOperator` dengan perintah `hdfs dfs -put`. Mengapa pipeline menggunakan pendekatan "buat file CSV dulu di `/tmp/`, lalu `put` ke HDFS" alih-alih langsung menulis ke HDFS dari script generator? Apa kelebihan dan kekurangan pendekatan ini?**

> Tulis jawaban Anda di sini:
>
> _..._

---

**R1.3 — Mekanisme XCom digunakan untuk mengirim nilai `jumlah_baris` dari task `validasi_data` ke task `cetak_laporan`. Jelaskan bagaimana XCom berbeda dari variabel global Python biasa dalam konteks eksekusi Airflow yang terdistribusi.**

> Tulis jawaban Anda di sini:
>
> _..._

---

**R1.4 — DAG ini menggunakan `schedule="@daily"` dengan `catchup=False`. Jika `catchup=True` dan DAG baru diaktifkan hari ini padahal `start_date` adalah satu bulan lalu, apa yang terjadi?**

> Tulis jawaban Anda di sini:
>
> _..._

---

**R1.5 — Dari Tabel 1.2, bandingkan durasi task `buat_file_simulasi` (BashOperator) dengan task `validasi_data` (PythonOperator). Secara umum, operator mana yang cenderung lebih cepat startup-nya dan mengapa?**

> Tulis jawaban Anda di sini:
>
> _..._

---

## Kesimpulan Latihan 1

> "DAG `latihan_pipeline_transaksi` berhasil dieksekusi dengan total **___** task dalam waktu **___** detik. Task `validasi_data` menemukan **___** baris data dan mengirimkan nilai ini ke task `cetak_laporan` melalui mekanisme **___** (XCom/variabel global). Alur eksekusi bersifat **___** (linear/paralel). Keunggulan utama Airflow yang terlihat dalam latihan ini adalah **___**."

---

*Latihan 1 selesai. Lanjutkan ke **Latihan 2 — Integrasi Airflow dengan Apache Spark**.*
