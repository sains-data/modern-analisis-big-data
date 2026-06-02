# Latihan 3 — Menjelajahi Apache Atlas
**Chapter 9 · Orkestrasi dan Tata Kelola Data** | Estimasi waktu: **20 menit**

---

## Tujuan Latihan

Setelah menyelesaikan latihan ini, mahasiswa mampu:
- Mendaftarkan entitas tabel Hive (Bronze dan Silver) ke Apache Atlas via REST API
- Menambahkan klasifikasi sensitivitas data (`PII`, `FINANSIAL`) pada entitas dan kolom
- Mengambil dan membaca informasi lineage dari Atlas
- Menggunakan Atlas Web UI untuk pencarian entitas dan visualisasi lineage
- Memahami konsep propagasi klasifikasi

---

## Prasyarat

- [ ] Latihan 1 dan 2 selesai
- [ ] Atlas berjalan: `curl -u admin:admin http://localhost:22100/api/atlas/admin/status` → HTTP 200
- [ ] Data Silver tersedia: `docker exec bigdata-spark hdfs dfs -ls /datalake/silver/latihan/`
- [ ] Python `requests` tersedia di host (`python3 -c "import requests"`)

---

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Atlas UI | http://localhost:22100 (`admin` / `admin`) |
| REST API base | `http://localhost:22100/api/atlas/v2` |
| Backend Atlas | JanusGraph (HBase) + Solr — stack Docker Chapter 9 |

> Port **22100** di host = port internal 21000 di container (selaras Data-Lakehouse-Metadata).

---

## Langkah Kerja

### Langkah 3.1 — Verifikasi koneksi ke Atlas REST API

```bash
curl -s -u admin:admin \
  http://localhost:22100/api/atlas/admin/status \
  | python3 -m json.tool

curl -s -u admin:admin \
  "http://localhost:22100/api/atlas/v2/types/typedefs" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
hive_types = [e['name'] for e in data.get('entityDefs', []) if 'hive' in e['name']]
print('Tipe Hive:', sorted(hive_types))
print('Total:', len(hive_types))
"
```

Catat pada **Tabel 3.1**.

---

### Langkah 3.2 — Buat dan jalankan script pendaftaran entitas

```bash
nano /tmp/daftar_entitas.py
```

```python
import requests
import json

BASE = "http://localhost:22100/api/atlas/v2"
AUTH = ("admin", "admin")
HDR = {"Content-Type": "application/json"}


def daftar_tabel(nama, db, deskripsi, kolom_list):
    kolom_entities = []
    for col in kolom_list:
        kolom_entities.append({
            "typeName": "hive_column",
            "attributes": {
                "name": col["name"],
                "type": col["type"],
                "qualifiedName": f"{db}.{nama}.{col['name']}@cluster1",
                "table": {
                    "typeName": "hive_table",
                    "uniqueAttributes": {
                        "qualifiedName": f"{db}.{nama}@cluster1"
                    }
                }
            }
        })

    payload = {
        "entities": [{
            "typeName": "hive_table",
            "attributes": {
                "name": nama,
                "qualifiedName": f"{db}.{nama}@cluster1",
                "db": {
                    "typeName": "hive_db",
                    "uniqueAttributes": {"qualifiedName": f"{db}@cluster1"}
                },
                "description": deskripsi,
                "owner": "mahasiswa",
                "tableType": "MANAGED_TABLE",
                "temporary": False,
            }
        }] + kolom_entities
    }

    resp = requests.post(f"{BASE}/entity/bulk", auth=AUTH, headers=HDR, data=json.dumps(payload))
    print(f"\n[DAFTAR] Tabel '{nama}' → HTTP {resp.status_code}")
    guids = resp.json().get("guidAssignments", {})
    print(f"  GUID diberikan: {len(guids)}")
    return guids


daftar_tabel(
    "transaksi_bronze", "datalake",
    "Tabel raw transaksi harian (Bronze layer)",
    [{"name": "id", "type": "string"}, {"name": "nilai", "type": "string"},
     {"name": "kategori", "type": "string"}],
)

daftar_tabel(
    "transaksi_silver", "datalake",
    "Tabel transaksi bersih (Silver layer)",
    [{"name": "id", "type": "string"}, {"name": "nilai", "type": "double"},
     {"name": "kategori", "type": "string"}, {"name": "tanggal_proses", "type": "string"}],
)

print("\n[OK] Pendaftaran selesai.")
```

```bash
python3 /tmp/daftar_entitas.py
```

---

### Langkah 3.3 — Tambahkan klasifikasi sensitivitas data

```bash
nano /tmp/klasifikasi_pii.py
```

```python
import requests
import json

BASE = "http://localhost:22100/api/atlas/v2"
AUTH = ("admin", "admin")
HDR = {"Content-Type": "application/json"}


def cari_guid(nama_tabel, nama_kolom=None):
    if nama_kolom:
        qn, tipe = f"datalake.{nama_tabel}.{nama_kolom}@cluster1", "hive_column"
    else:
        qn, tipe = f"datalake.{nama_tabel}@cluster1", "hive_table"
    resp = requests.get(
        f"{BASE}/entity/uniqueAttribute/type/{tipe}",
        auth=AUTH, params={"attr:qualifiedName": qn},
    )
    if resp.status_code != 200:
        print(f"  [TIDAK DITEMUKAN] {qn}")
        return None
    guid = resp.json()["entity"]["guid"]
    print(f"  [DITEMUKAN] {qn} → {guid}")
    return guid


def tambah_klasifikasi(guid, nama_klasifikasi, propagate=True):
    payload = [{
        "typeName": nama_klasifikasi,
        "propagate": propagate,
        "removePropagationsOnEntityDelete": True,
    }]
    resp = requests.post(
        f"{BASE}/entity/guid/{guid}/classifications",
        auth=AUTH, headers=HDR, data=json.dumps(payload),
    )
    ok = resp.status_code in (200, 204)
    print(f"  Klasifikasi [{nama_klasifikasi}] → {'OK' if ok else resp.status_code}")
    return resp.status_code


print("\n=== Kolom id Bronze ===")
g = cari_guid("transaksi_bronze", "id")
if g:
    tambah_klasifikasi(g, "PII", True)

print("\n=== Kolom id Silver ===")
g = cari_guid("transaksi_silver", "id")
if g:
    tambah_klasifikasi(g, "PII", True)

print("\n=== Tabel Silver ===")
g = cari_guid("transaksi_silver")
if g:
    tambah_klasifikasi(g, "FINANSIAL", False)

print("\n=== Kolom nilai Silver ===")
g = cari_guid("transaksi_silver", "nilai")
if g:
    tambah_klasifikasi(g, "SENSITIF", True)

print("\n[OK] Klasifikasi selesai.")
```

```bash
python3 /tmp/klasifikasi_pii.py
```

---

### Langkah 3.4 — Script lineage

```bash
nano /tmp/ambil_lineage.py
```

```python
import requests

BASE = "http://localhost:22100/api/atlas/v2"
AUTH = ("admin", "admin")


def cari_guid_tabel(nama):
    resp = requests.get(
        f"{BASE}/entity/uniqueAttribute/type/hive_table",
        auth=AUTH,
        params={"attr:qualifiedName": f"datalake.{nama}@cluster1"},
    )
    return resp.json()["entity"]["guid"] if resp.status_code == 200 else None


def tampilkan_lineage(nama_tabel, direction="BOTH"):
    guid = cari_guid_tabel(nama_tabel)
    if not guid:
        print(f"[ERROR] Tidak ditemukan: {nama_tabel}")
        return
    resp = requests.get(
        f"{BASE}/lineage/{guid}", auth=AUTH,
        params={"direction": direction, "depth": 5},
    )
    data = resp.json()
    entitas = data.get("guidEntityMap", {})
    relasi = data.get("relations", [])
    print(f"\nLineage {nama_tabel}: {len(entitas)} entitas, {len(relasi)} relasi")
    for rel in relasi:
        print(f"  {rel.get('fromEntityId','?')[:8]} → {rel.get('toEntityId','?')[:8]}")
    if not relasi:
        print("  [INFO] Belum ada relasi — normal sebelum Latihan 4.")


tampilkan_lineage("transaksi_silver", "BOTH")
tampilkan_lineage("transaksi_bronze", "OUTPUT")
```

```bash
python3 /tmp/ambil_lineage.py
```

Catat pada **Tabel 3.3**.

---

### Langkah 3.5 — Verifikasi melalui Atlas Web UI

Buka `http://localhost:22100`. Login `admin / admin`.

1. **Search** → Entity Type `hive_table` → cari `transaksi_bronze` dan `transaksi_silver`
2. Periksa tab **Properties**, **Classifications**, **Lineage**

Catat pada **Tabel 3.4**.

---

### Langkah 3.6 — Cari entitas berdasarkan klasifikasi

```bash
python3 << 'EOF'
import requests

BASE = "http://localhost:22100/api/atlas/v2"
AUTH = ("admin", "admin")

resp = requests.get(f"{BASE}/search/basic", auth=AUTH, params={
    "classification": "PII", "typeName": "hive_column", "limit": 20,
})
results = resp.json()
print(f"Kolom dengan PII: {results.get('count', 0)}")
for ent in results.get("entities", []):
    print(f"  {ent.get('attributes', {}).get('name')}")

resp2 = requests.get(f"{BASE}/search/basic", auth=AUTH, params={
    "classification": "FINANSIAL", "limit": 20,
})
print(f"\nEntitas FINANSIAL: {resp2.get('count', 0)}")
EOF
```

---

## Tabel Pencatatan Hasil

### Tabel 3.1 — Tipe Entitas Hive di Atlas

| Tipe | Ada? |
|---|---|
| `hive_table` | Ya / Tidak |
| `hive_column` | Ya / Tidak |
| `hive_db` | Ya / Tidak |
| `spark_process` | Ya / Tidak |

### Tabel 3.2 — Pendaftaran & Klasifikasi

| Entitas | HTTP Status | Klasifikasi | Propagate |
|---|---|---|---|
| transaksi_bronze / id | _..._ | PII | True |
| transaksi_silver / id | _..._ | PII | True |
| transaksi_silver (tabel) | _..._ | FINANSIAL | False |
| transaksi_silver / nilai | _..._ | SENSITIF | True |

### Tabel 3.3 — Lineage & Pencarian

| Perspektif | Entitas | Relasi | Catatan |
|---|---|---|---|
| transaksi_silver (BOTH) | _..._ | _..._ | _..._ |
| PII (search) | _..._ | — | _..._ |

### Tabel 3.4 — Pengamatan Atlas UI

| Aspek | Bronze | Silver |
|---|---|---|
| qualifiedName | _..._ | _..._ |
| Classifications | _..._ | _..._ |
| Lineage ada? | Ya/Tidak | Ya/Tidak |

---

## Refleksi dan Analisis

**R3.1 — Apakah lineage Bronze→Silver sudah otomatis? Jika belum, komponen apa yang belum aktif?**

> _..._

**R3.2 — Perbedaan `propagate=True` vs `propagate=False`?**

> _..._

**R3.3 — Mengapa kolom didaftarkan terpisah dari tabel?**

> _..._

**R3.4 — Mengapa metadata Atlas disimpan sebagai graf?**

> _..._

**R3.5 — Tiga kemungkinan penyebab HTTP 404 saat `cari_guid()`?**

> _..._

---

## Kesimpulan Latihan 3

> "Dua entitas terdaftar di Atlas (`transaksi_bronze`, `transaksi_silver`). Klasifikasi **___** diterapkan dengan propagasi **___**. Lineage saat ini **___** karena **___**."

---

*Latihan 3 selesai. Lanjutkan ke **Latihan 4 — Pipeline End-to-End Terintegrasi**.*
