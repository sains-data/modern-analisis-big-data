# Latihan 5 — Eksplorasi Lanjutan: Retry, Pencarian Atlas, dan Diskusi
**Chapter 9 · Orkestrasi dan Tata Kelola Data** | Estimasi waktu: **15 menit**

---

## Tujuan Latihan

Setelah menyelesaikan latihan ini, mahasiswa mampu:
- Menguji mekanisme **retry** Airflow pada task yang tidak stabil
- Melakukan **pencarian metadata** di Atlas (basic search & attribute search)
- Mendiskusikan desain pipeline, propagasi klasifikasi, dan impact analysis

---

## Prasyarat

- [ ] Latihan 1–4 selesai
- [ ] Airflow UI: http://localhost:18681
- [ ] Atlas UI / API: http://localhost:22100
- [ ] Entitas dan klasifikasi dari Latihan 3 masih ada di Atlas

---

## Tugas A — Simulasi Kegagalan dan Retry

Tambahkan task berikut ke DAG latihan (salin ke `Konfigurasi-lab/dags/latihan_retry_demo.py` atau sisipkan ke DAG existing):

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
import random

default_args = {"owner": "mahasiswa", "retries": 0}


def task_tidak_stabil(**context):
    if random.random() < 0.7:
        raise RuntimeError("Simulasi kegagalan: koneksi database gagal!")
    print("[SUKSES] Task berhasil pada percobaan ini.")


with DAG(
    dag_id="latihan_retry_demo",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["latihan", "chapter9", "retry"],
) as dag:

    mulai = EmptyOperator(task_id="mulai")

    task_flaky = PythonOperator(
        task_id="task_tidak_stabil",
        python_callable=task_tidak_stabil,
        retries=4,
        retry_delay=timedelta(seconds=10),
    )

    selesai = EmptyOperator(task_id="selesai")
    mulai >> task_flaky >> selesai
```

Trigger dan amati retry:

```bash
docker exec modul7-airflow-scheduler airflow dags trigger latihan_retry_demo
```

Buka `http://localhost:18681` → DAG `latihan_retry_demo` → log task → hitung berapa kali retry sebelum sukses/gagal.

| Percobaan | Status | Catatan |
|---|---|---|
| 1 | _..._ | _..._ |
| 2 | _..._ | _..._ |
| ... | _..._ | _..._ |

---

## Tugas B — Pencarian Metadata Atlas

Jalankan dari terminal host (`BASE` memakai port **22100**):

```python
import requests
import json

BASE = "http://localhost:22100/api/atlas/v2"
AUTH = ("admin", "admin")

# Cari entitas dengan klasifikasi PII
query = {
    "typeName": "hive_table",
    "classification": "PII",
    "limit": 20,
    "offset": 0,
}
resp = requests.post(
    f"{BASE}/search/dsl",
    auth=AUTH,
    headers={"Content-Type": "application/json"},
    data=json.dumps(query),
)
results = resp.json()
print(f"Entitas PII (DSL): {results.get('count', 0)}")

# Cari tabel di database datalake
resp2 = requests.get(
    f"{BASE}/search/attribute",
    auth=AUTH,
    params={
        "typeName": "hive_table",
        "attrName": "db.qualifiedName",
        "attrValuePrefix": "datalake",
        "limit": 20,
    },
)
results2 = resp2.json()
print(f"\nTabel di database datalake: {len(results2.get('entities', []))}")
for ent in results2.get("entities", []):
    print(f"  {ent.get('attributes', {}).get('name')}")
```

Simpan script sebagai `/tmp/cari_metadata_atlas.py` dan jalankan:

```bash
python3 /tmp/cari_metadata_atlas.py
```

| Pencarian | Jumlah Hasil | Contoh Entitas |
|---|---|---|
| Klasifikasi PII (DSL) | _..._ | _..._ |
| Tabel prefix `datalake` | _..._ | _..._ |

---

## Tugas C — Pertanyaan Diskusi

Jawab singkat (3–5 kalimat per pertanyaan):

**C1.** Apa fungsi arsitektural `EmptyOperator` pada task `mulai` / `selesai`?

> _..._

**C2.** Apa yang terjadi jika `catchup=True` dan `start_date` satu bulan lalu?

> _..._

**C3.** Mengapa propagasi klasifikasi `PII` penting untuk audit regulasi?

> _..._

**C4.** Prasyarat task paralel di Latihan 4 — kapan dua task **tidak** aman dijalankan paralel?

> _..._

**C5.** Kolom `nilai` di Bronze diubah tipe `string` → `double`. Bagaimana lineage Atlas membantu impact analysis?

> _..._

---

## Kesimpulan Chapter 9

Setelah lima latihan, lengkapi pernyataan:

> "Chapter 9 mengintegrasikan **___** (orkestrasi), **___** (komputasi via bigdata-spark), dan **___** (governance metadata). Airflow diakses di port **___** dengan kredensial **___** / **___**. Atlas diakses di port **___** dengan backend **___** + **___** (bukan BerkeleyDB embedded). Pipeline E2E menunjukkan pola **___** untuk paralelisasi task independen."

---

*Latihan 5 selesai. Chapter 9 praktik tuntas.*
