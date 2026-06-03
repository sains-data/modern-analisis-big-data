# Latihan 1 — Persiapan Data dan Eksplorasi Awal
**Chapter 11 · Machine Learning Big Data** | Estimasi waktu: **10 menit**

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Kontainer `bigdata-spark` berjalan
- [ ] HDFS UI (`http://localhost:9870`) dan YARN UI (`http://localhost:8088`) dapat diakses
- [ ] Referensi data — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Referensi data

| Sumber | Volume | Catatan |
|--------|--------|---------|
| HDFS Silver | **10.000 baris** | Runtime (`init_data.sh`) |
| `Data/transaksi_ml.csv` | 10.000 | Referensi statis copula |
| Partisipan unik | **200** | `usr-0001` … `usr-0200` |

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Folder kerja | `Konfigurasi-lab/` |
| Kontainer | `bigdata-spark` |
| Generator data | `scripts/buat_data_ml.py` |
| Path Silver | `hdfs:///datalake/silver/transaksi/` |

> Semua perintah dijalankan dari folder **`Konfigurasi-lab/`**.

## Langkah Kerja

### 1) Jalankan stack

```bash
cd ../Konfigurasi-lab
bash start.sh
```

### 2) Generate data latihan

```bash
bash scripts/init_data.sh
```

### 3) Verifikasi data di HDFS

```bash
docker exec bigdata-spark hdfs dfs -ls /datalake/silver/transaksi/
docker exec bigdata-spark hdfs dfs -du -h /datalake/silver/transaksi/
docker exec bigdata-spark hdfs dfs -ls /datalake/bronze/transaksi/
```

### 4) Eksplorasi cepat via PySpark

```bash
docker exec -it bigdata-spark pyspark --master yarn --executor-memory 512m --num-executors 2
```

```python
from pyspark.sql import functions as F
df = spark.read.parquet("hdfs:///datalake/silver/transaksi/")
print(df.count(), len(df.columns))
df.select("kuantitas", "harga_satuan", "diskon", "total_nilai").describe().show()
df.groupBy("kategori").count().orderBy(F.col("count").desc()).show()
```

## Pencatatan Hasil

- Jumlah baris dataset (**10.000**)
- Jumlah kolom (**9** di Silver; `segmen` dihitung saat ML)
- Ukuran data Silver di HDFS
- Distribusi kategori transaksi (6 kelas)

---

*Latihan 1 selesai. Lanjut ke **Latihan 2 — Supervised Learning: Regresi dan Klasifikasi**.*
