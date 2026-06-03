# Latihan 4 — Pipeline End-to-End Terintegrasi
**Chapter 9 · Orkestrasi dan Tata Kelola Data** | Estimasi waktu: **25 menit**

---

## Tujuan Latihan

Setelah menyelesaikan latihan ini, mahasiswa mampu:
- Membangun DAG yang mengintegrasikan HDFS, Spark, Hive, dan Atlas
- Merancang task paralel dengan sintaks `>> [task_a, task_b]`
- Mendaftarkan lineage `spark_process` ke Atlas dari dalam DAG
- Menjalankan agregasi Silver → Gold
- Mengamati pola fan-out / fan-in di Airflow UI

---

## Prasyarat

- [ ] Latihan 1–3 selesai
- [ ] Entitas Atlas `transaksi_bronze` dan `transaksi_silver` terdaftar
- [ ] Skrip `/opt/spark-jobs/latihan_etl.py` dan `pipeline_gold.py` ada di `bigdata-spark`
- [ ] Silver ~97 baris, Gold agregat per kategori — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)
- [ ] (Opsional Latihan 4) HiveServer2 exposed di port `10000` — lihat [Konfigurasi-lab §3.2](../Konfigurasi-lab/README.md#32--opsional-expose-hiveserver2-untuk-latihan-4)

---

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Airflow UI | http://localhost:18681 |
| Atlas REST | `http://localhost:22100/api/atlas/v2` |
| Path DAG | `Konfigurasi-lab/dags/pipeline_e2e.py` |

---

## Langkah Kerja

### Langkah 4.1 — Arsitektur pipeline

```
mulai → ingest_bronze → spark_etl → [hive_load_silver, registrasi_atlas] → spark_gold → validasi → selesai
```

---

### Langkah 4.2 — Buat tabel Hive Silver (prasyarat)

```bash
docker exec bigdata-spark hive -e "
CREATE DATABASE IF NOT EXISTS datalake;

CREATE EXTERNAL TABLE IF NOT EXISTS datalake.transaksi_silver (
    id             STRING,
    nilai          DOUBLE,
    kategori       STRING,
    tanggal_proses STRING
)
PARTITIONED BY (tanggal STRING)
STORED AS PARQUET
LOCATION 'hdfs:///datalake/silver/latihan/';
"

docker exec bigdata-spark hive -e "SHOW TABLES IN datalake;"
```

---

### Langkah 4.3 — Buat DAG pipeline end-to-end

```bash
nano Konfigurasi-lab/dags/pipeline_e2e.py
```

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
import requests
import json
import subprocess

BIGDATA = "/opt/airflow/scripts/bigdata_exec.sh"
ATLAS_URL = "http://host.docker.internal:22100/api/atlas/v2"
ATLAS_AUTH = ("admin", "admin")
ATLAS_HDR = {"Content-Type": "application/json"}

default_args = {
    "owner": "mahasiswa",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def daftar_lineage_ke_atlas(**context):
    tanggal = context["ds"]
    payload = {
        "entities": [{
            "typeName": "spark_process",
            "attributes": {
                "name": f"ETL-Bronze-Silver-{tanggal}",
                "qualifiedName": f"spark.etl.bronze_silver.{tanggal}@cluster1",
                "description": f"Spark ETL Bronze → Silver, tanggal {tanggal}",
                "inputs": [{
                    "typeName": "hive_table",
                    "uniqueAttributes": {
                        "qualifiedName": "datalake.transaksi_bronze@cluster1"
                    }
                }],
                "outputs": [{
                    "typeName": "hive_table",
                    "uniqueAttributes": {
                        "qualifiedName": "datalake.transaksi_silver@cluster1"
                    }
                }],
                "userName": "mahasiswa",
            }
        }]
    }
    resp = requests.post(
        f"{ATLAS_URL}/entity/bulk",
        auth=ATLAS_AUTH, headers=ATLAS_HDR, data=json.dumps(payload),
    )
    print(f"[ATLAS] HTTP {resp.status_code}")
    if resp.status_code in (200, 201):
        guids = resp.json().get("guidAssignments", {})
        guid = list(guids.values())[0] if guids else None
        context["ti"].xcom_push(key="atlas_process_guid", value=guid)
        print(f"[ATLAS] GUID proses: {guid}")


def validasi_gold(**context):
    result = subprocess.run(
        ["docker", "exec", "bigdata-spark", "hdfs", "dfs", "-ls",
         "/datalake/gold/latihan/"],
        capture_output=True, text=True, check=True,
    )
    print(result.stdout)
    atlas_guid = context["ti"].xcom_pull(
        task_ids="registrasi_atlas", key="atlas_process_guid"
    )
    print(f"[VALIDASI GOLD] GUID Atlas: {atlas_guid}")


with DAG(
    dag_id="pipeline_e2e_terintegrasi",
    default_args=default_args,
    description="Pipeline end-to-end: Spark + Hive + Atlas",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["latihan", "chapter9", "e2e"],
) as dag:

    mulai = EmptyOperator(task_id="mulai")

    ingest = BashOperator(
        task_id="ingest_bronze",
        bash_command=(
            f"{BIGDATA} "
            "'python /opt/scripts/generate_data.py {{ ds }} 100 "
            "> /tmp/transaksi_{{ ds_nodash }}.csv && "
            "hdfs dfs -mkdir -p /datalake/bronze/latihan/ && "
            "hdfs dfs -put -f /tmp/transaksi_{{ ds_nodash }}.csv "
            "/datalake/bronze/latihan/'"
        ),
    )

    spark_etl = SparkSubmitOperator(
        task_id="spark_etl",
        application="/opt/spark-jobs/latihan_etl.py",
        conn_id="spark_default",
        application_args=["{{ ds }}"],
        conf={"spark.sql.shuffle.partitions": "10"},
        executor_memory="512m",
        num_executors=2,
        verbose=True,
        name="airflow-etl-e2e-{{ ds_nodash }}",
    )

    hive_load = BashOperator(
        task_id="hive_load_silver",
        bash_command=(
            f"{BIGDATA} "
            "\"hive -e 'MSCK REPAIR TABLE datalake.transaksi_silver; "
            "SELECT COUNT(*) FROM datalake.transaksi_silver;'\""
        ),
    )

    atlas_register = PythonOperator(
        task_id="registrasi_atlas",
        python_callable=daftar_lineage_ke_atlas,
    )

    spark_gold = SparkSubmitOperator(
        task_id="spark_gold_agregasi",
        application="/opt/spark-jobs/pipeline_gold.py",
        conn_id="spark_default",
        application_args=["{{ ds }}"],
        conf={"spark.sql.shuffle.partitions": "10"},
        executor_memory="512m",
        num_executors=2,
        verbose=True,
        name="airflow-gold-e2e-{{ ds_nodash }}",
    )

    validasi = PythonOperator(
        task_id="validasi_output_gold",
        python_callable=validasi_gold,
    )

    selesai = EmptyOperator(task_id="selesai")

    mulai >> ingest >> spark_etl >> [hive_load, atlas_register] >> spark_gold >> validasi >> selesai
```

> **Catatan Atlas URL di DAG:** task Python di scheduler memakai `host.docker.internal:22100` agar container Airflow dapat menjangkau Atlas di host (port map 22100).

---

### Langkah 4.4 — Trigger DAG dan pantau

```bash
sleep 15
docker exec modul7-airflow-scheduler airflow dags trigger pipeline_e2e_terintegrasi

RUN_ID=$(docker exec modul7-airflow-scheduler airflow dags list-runs \
  pipeline_e2e_terintegrasi --output json 2>/dev/null \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d[0]['run_id'])")

watch -n 30 "docker exec modul7-airflow-scheduler airflow tasks states-for-dag-run \
  pipeline_e2e_terintegrasi '$RUN_ID'"
```

---

### Langkah 4.5 — Amati tab Graph di Airflow UI

Buka `http://localhost:18681` → `pipeline_e2e_terintegrasi` → **Graph**.

Periksa pola fan-out dari `spark_etl` dan fan-in ke `spark_gold_agregasi`. Catat **Tabel 4.2**.

---

### Langkah 4.6 — Baca log task penting

```bash
docker exec modul7-airflow-scheduler airflow tasks logs \
  pipeline_e2e_terintegrasi registrasi_atlas "$RUN_ID" 1

docker exec modul7-airflow-scheduler airflow tasks logs \
  pipeline_e2e_terintegrasi spark_gold_agregasi "$RUN_ID" 1
```

---

### Langkah 4.7 — Verifikasi HDFS dan Atlas

```bash
docker exec bigdata-spark hdfs dfs -ls /datalake/gold/latihan/
python3 /tmp/ambil_lineage.py
```

---

### Langkah 4.8 — Verifikasi lineage di Atlas UI

Buka `http://localhost:22100` → Search → `transaksi_silver` → tab **Lineage**.

Apakah node `spark_process` muncul setelah pipeline? Catat **Tabel 4.4**.

---

## Tabel Pencatatan Hasil

### Tabel 4.1 — Status Infrastruktur

| Komponen | Status |
|---|---|
| Hive `datalake.transaksi_silver` | Ada / Tidak |
| Entitas Atlas Bronze + Silver | Ada / Tidak |
| Koneksi `spark_default` | Ada / Tidak |

### Tabel 4.2 — Status & Durasi Task

| Task | Status | Durasi | Paralel dengan |
|---|---|---|---|
| `hive_load_silver` | _..._ | _..._ | `registrasi_atlas` |
| `registrasi_atlas` | _..._ | _..._ | `hive_load_silver` |
| `spark_gold_agregasi` | _..._ | _..._ | — |
| **Total** | — | **_..._ s** | — |

### Tabel 4.3 — Output & Log

| Layer | Path | File | Ukuran |
|---|---|---|---|
| Gold | `/datalake/gold/latihan/` | _..._ | _..._ |

| Log `registrasi_atlas` | Nilai |
|---|---|
| HTTP status | _..._ |
| GUID proses | _..._ |

### Tabel 4.4 — UI

| Pengamatan | Sebelum (Lat. 3) | Sesudah (Lat. 4) |
|---|---|---|
| Lineage Silver | _..._ | _..._ |
| Entitas `spark_process` | Tidak | Ya / Tidak |

---

## Refleksi dan Analisis

**R4.1 — Prasyarat task paralel `hive_load` dan `registrasi_atlas`?**

> _..._

**R4.2 — Mengapa registrasi lineage penting untuk impact analysis?**

> _..._

**R4.3 — Kapan `spark_gold` bisa mulai jika satu task paralel lambat?**

> _..._

**R4.4 — Bagaimana desain Gold agar historis per hari (bukan overwrite)?**

> _..._

**R4.5 — Bagaimana agar kegagalan Atlas tidak menghentikan `spark_gold`? (`trigger_rule`)**

> _..._

---

## Kesimpulan Latihan 4

> "Pipeline E2E berhasil dengan **___** task, **___** task paralel, durasi **___** detik. Lineage terdaftar via entitas **___**. Gold layer berisi **___** kategori."

---

*Latihan 4 selesai. Lanjutkan ke **Latihan 5 — Eksplorasi Lanjutan**.*
