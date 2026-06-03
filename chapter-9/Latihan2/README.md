# Latihan 2 — Integrasi Airflow dengan Apache Spark
**Chapter 9 · Orkestrasi dan Tata Kelola Data** | Estimasi waktu: **25 menit**

---

## Tujuan Latihan

Setelah menyelesaikan latihan ini, mahasiswa mampu:
- Membuat Spark job Python untuk transformasi data CSV (Bronze) menjadi Parquet (Silver)
- Mengintegrasikan Spark job ke dalam DAG Airflow menggunakan `SparkSubmitOperator`
- Mengonfigurasi koneksi `spark_default` yang memanggil `spark-submit` di `bigdata-spark`
- Membaca log Spark job dari Airflow UI
- Memverifikasi output Parquet di HDFS Silver layer

---

## Prasyarat

- [ ] Latihan 1 selesai dan DAG `latihan_pipeline_transaksi` berstatus success
- [ ] Data tersedia di `hdfs:///datalake/bronze/latihan/` (**100 baris** per run)
- [ ] Koneksi `spark_default` terdaftar (`docker exec modul7-airflow-scheduler airflow connections get spark_default`)
- [ ] File `/opt/spark-jobs/latihan_etl.py` ada di `bigdata-spark` (via `setup_bigdata_spark.sh`)
- [ ] Volume harapan ETL — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md): **100 raw → ~97 valid → 3 ditolak**

---

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Airflow UI | http://localhost:18681 |
| Spark job | `/opt/spark-jobs/latihan_etl.py` (di `bigdata-spark`) |
| Koneksi Spark | `spark_default` → `spark_submit_bigdata.sh` |
| Path DAG | `Konfigurasi-lab/dags/latihan_pipeline_spark.py` |

---

## Langkah Kerja

### Langkah 2.1 — Verifikasi Spark job tersedia

```bash
docker exec bigdata-spark ls -lh /opt/spark-jobs/latihan_etl.py
docker exec bigdata-spark head -20 /opt/spark-jobs/latihan_etl.py

docker exec modul7-airflow-scheduler airflow connections get spark_default
```

Output koneksi harus menampilkan `spark-binary` = `/opt/airflow/scripts/spark_submit_bigdata.sh`.

---

### Langkah 2.2 — Uji Spark job secara manual (tanpa Airflow)

```bash
docker exec bigdata-spark hdfs dfs -ls /datalake/bronze/latihan/

docker exec bigdata-spark spark-submit \
  --master yarn \
  --deploy-mode client \
  --executor-memory 512m \
  --num-executors 2 \
  --conf spark.sql.shuffle.partitions=10 \
  /opt/spark-jobs/latihan_etl.py \
  $(date +%Y-%m-%d)
```

Catat `[ETL] Baris raw`, `valid`, `ditolak` pada **Tabel 2.1**.

```bash
docker exec bigdata-spark hdfs dfs -ls /datalake/silver/latihan/
docker exec bigdata-spark hdfs dfs -du -s -h /datalake/silver/latihan/
```

---

### Langkah 2.3 — Buat DAG baru dengan SparkSubmitOperator

```bash
nano Konfigurasi-lab/dags/latihan_pipeline_spark.py
```

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
import subprocess

BIGDATA = "/opt/airflow/scripts/bigdata_exec.sh"

default_args = {
    "owner": "mahasiswa",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def validasi_output_silver(**context):
    result = subprocess.run(
        ["docker", "exec", "bigdata-spark", "hdfs", "dfs", "-ls",
         "/datalake/silver/latihan/"],
        capture_output=True, text=True, check=True,
    )
    lines = result.stdout.strip().split("\n")
    print(f"[VALIDASI OUTPUT] File di Silver layer: {len(lines) - 1}")
    print(result.stdout)
    context["ti"].xcom_push(key="jumlah_file_silver", value=len(lines) - 1)


def cetak_ringkasan(**context):
    n_file = context["ti"].xcom_pull(
        task_ids="validasi_output_silver", key="jumlah_file_silver"
    )
    print(f"[RINGKASAN] Tanggal  : {context['ds']}")
    print(f"[RINGKASAN] File Silver: {n_file}")
    print("[RINGKASAN] Pipeline Spark ETL SELESAI.")


with DAG(
    dag_id="latihan_pipeline_spark",
    default_args=default_args,
    description="DAG latihan Airflow + Spark ETL",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["latihan", "chapter9", "spark"],
) as dag:

    mulai = EmptyOperator(task_id="mulai")

    buat_dan_ingest = BashOperator(
        task_id="buat_dan_ingest_bronze",
        bash_command=(
            f"{BIGDATA} "
            "'python /opt/scripts/generate_data.py {{ ds }} 100 "
            "> /tmp/transaksi_{{ ds_nodash }}.csv && "
            "hdfs dfs -mkdir -p /datalake/bronze/latihan/ && "
            "hdfs dfs -put -f /tmp/transaksi_{{ ds_nodash }}.csv "
            "/datalake/bronze/latihan/ && "
            "hdfs dfs -ls /datalake/bronze/latihan/'"
        ),
    )

    spark_etl = SparkSubmitOperator(
        task_id="spark_etl_bronze_silver",
        application="/opt/spark-jobs/latihan_etl.py",
        conn_id="spark_default",
        application_args=["{{ ds }}"],
        conf={"spark.executor.memory": "512m", "spark.sql.shuffle.partitions": "10"},
        executor_memory="512m",
        num_executors=2,
        verbose=True,
        name="airflow-etl-{{ ds_nodash }}",
    )

    validasi = PythonOperator(
        task_id="validasi_output_silver",
        python_callable=validasi_output_silver,
    )

    ringkasan = PythonOperator(
        task_id="cetak_ringkasan",
        python_callable=cetak_ringkasan,
    )

    selesai = EmptyOperator(task_id="selesai")

    mulai >> buat_dan_ingest >> spark_etl >> validasi >> ringkasan >> selesai
```

---

### Langkah 2.4 — Trigger DAG Spark dan pantau eksekusi

```bash
sleep 15
docker exec modul7-airflow-scheduler airflow dags list | grep latihan_pipeline_spark
docker exec modul7-airflow-scheduler airflow dags trigger latihan_pipeline_spark

watch -n 30 "docker exec modul7-airflow-scheduler airflow dags list-runs latihan_pipeline_spark"
```

---

### Langkah 2.5 — Baca log task Spark ETL

```bash
RUN_ID=$(docker exec modul7-airflow-scheduler airflow dags list-runs \
  latihan_pipeline_spark --output json 2>/dev/null \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d[0]['run_id'])")

docker exec modul7-airflow-scheduler airflow tasks logs \
  latihan_pipeline_spark spark_etl_bronze_silver "$RUN_ID" 1
```

Cari baris `[ETL] Baris raw/valid/ditolak` — catat pada **Tabel 2.2**.

---

### Langkah 2.6 — Amati tab Graph di Airflow UI

Buka `http://localhost:18681` → DAG `latihan_pipeline_spark` → tab **Graph**.

Catat pada **Tabel 2.3**.

---

### Langkah 2.7 — Verifikasi output Silver layer di HDFS

```bash
docker exec bigdata-spark hdfs dfs -ls /datalake/silver/latihan/
docker exec bigdata-spark hdfs dfs -du -s -h /datalake/silver/latihan/

docker exec bigdata-spark pyspark --master yarn --executor-memory 512m --num-executors 1 << 'EOF'
df = spark.read.parquet("hdfs:///datalake/silver/latihan/")
print(f"Total baris Silver: {df.count()}")
df.show(5, truncate=False)
df.printSchema()
exit()
EOF
```

---

## Tabel Pencatatan Hasil

### Tabel 2.1 — Hasil Spark ETL (manual + Airflow)

| Metrik | Manual (`spark-submit`) | Via Airflow DAG |
|---|---|---|
| Baris raw | _100_ | _100_ |
| Baris valid | _~97_ | _~97_ |
| Baris ditolak | _~3_ (~3%) | _~3_ (~3%) |
| Persentase ditolak | _..._% | _..._% |
| Jumlah file Silver | _..._ | _..._ |
| Ukuran Silver | _..._ | _..._ |

**Konsisten?** Ya / Tidak — _..._

### Tabel 2.2 — Durasi dan Status Task

| Task | Status | Durasi (detik) | Baris Kunci Log |
|---|---|---|---|
| `spark_etl_bronze_silver` | _..._ | _..._ | `[ETL] Baris valid: ...` |
| _(task lain)_ | _..._ | _..._ | _..._ |
| **Total pipeline** | — | **_..._ detik** | — |

### Tabel 2.3 — Pengamatan Airflow UI

| Aspek | Nilai |
|---|---|
| Task terlama | `spark_etl_bronze_silver` / _..._ detik |
| Log Spark terlihat di Airflow? | Ya / Tidak |
| Output Silver terverifikasi? | Ya / Tidak |

### Tabel 2.4 — Manual vs Airflow

| Aspek | Manual | Via Airflow |
|---|---|---|
| Log tersimpan | Terminal | Airflow UI (persisten) |
| Retry otomatis | Tidak | Ya (`retries=1`) |
| Dependensi task | Manual | Otomatis (DAG) |

---

## Refleksi dan Analisis

**R2.1 — Berapa persen data ditolak? Apakah konsisten dengan desain ~3% baris invalid?**

> _..._

**R2.2 — Mengapa task Spark paling lama? Sebutkan tiga tahap sebelum Spark memproses data.**

> _..._

**R2.3 — Bagaimana persistensi log Airflow membantu debugging tim?**

> _..._

**R2.4 — Mengapa `mode("overwrite")` penting untuk pipeline terjadwal?**

> _..._

**R2.5 — Berapa total memori Spark dengan `num_executors=2` dan `512m`? Apa risiko jika dinaikkan drastis?**

> _..._

---

## Kesimpulan Latihan 2

> "Pipeline Spark ETL diintegrasikan ke Airflow menggunakan **___**. Dari **___** baris raw, **___** baris valid ditulis ke Silver (**___**). Task Spark membutuhkan **___** detik karena **___**."

---

*Latihan 2 selesai. Lanjutkan ke **Latihan 3 — Menjelajahi Apache Atlas**.*
