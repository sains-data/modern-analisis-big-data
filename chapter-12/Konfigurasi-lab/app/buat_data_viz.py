"""Dataset transaksi 15.000 baris, 12 bulan — Bab 12 Tahap 1."""
import random
import uuid
from datetime import date

from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from spark_common import create_spark

KATEGORI = ["elektronik", "fashion", "makanan", "kesehatan", "otomotif"]
CHANNEL = ["mobile", "web", "atm", "teller"]
KOTA = [
    "Jakarta",
    "Surabaya",
    "Bandung",
    "Medan",
    "Makassar",
    "Semarang",
    "Palembang",
    "Yogyakarta",
    "Depok",
    "Tangerang",
]
N = 15_000
SILVER = "hdfs:///datalake/silver/transaksi/"


def main() -> None:
    random.seed(42)
    spark = create_spark("BuatDataViz")

    rows = []
    for _ in range(N):
        kat = random.choice(KATEGORI)
        bulan = random.randint(1, 12)
        tahun = 2024
        tanggal = date(tahun, bulan, random.randint(1, 28))
        base = {
            "elektronik": 500_000,
            "otomotif": 700_000,
            "fashion": 200_000,
            "makanan": 50_000,
            "kesehatan": 150_000,
        }[kat]
        mult = 1.4 if bulan == 11 else (1.1 if bulan == 12 else 1.0)
        qty = random.randint(1, 15)
        harga = base * random.uniform(0.5, 3.0) * mult
        diskon = random.uniform(0, 0.25)
        total = qty * harga * (1 - diskon)
        rows.append(
            (
                str(uuid.uuid4())[:8],
                f"usr-{random.randint(1, 300):04d}",
                kat,
                random.choice(CHANNEL),
                random.choice(KOTA),
                qty,
                round(harga, 2),
                round(diskon, 3),
                round(total, 2),
                tahun,
                bulan,
                str(tanggal),
            )
        )

    schema = StructType(
        [
            StructField("id_transaksi", StringType(), True),
            StructField("id_pelanggan", StringType(), True),
            StructField("kategori", StringType(), True),
            StructField("channel", StringType(), True),
            StructField("kota", StringType(), True),
            StructField("kuantitas", IntegerType(), True),
            StructField("harga_satuan", DoubleType(), True),
            StructField("diskon", DoubleType(), True),
            StructField("total_nilai", DoubleType(), True),
            StructField("tahun", IntegerType(), True),
            StructField("bulan", IntegerType(), True),
            StructField("tanggal", StringType(), True),
        ]
    )

    df = spark.createDataFrame(rows, schema=schema)
    df = df.withColumn("tanggal_transaksi", F.to_date("tanggal", "yyyy-MM-dd"))

    df.write.mode("overwrite").parquet(SILVER)
    print(f"[OK] Dataset: {df.count():,} baris → {SILVER}")
    df.groupBy("bulan").agg(
        F.count("*").alias("n"),
        F.round(F.sum("total_nilai") / 1e6, 2).alias("omzet_juta"),
    ).orderBy("bulan").show()

    spark.stop()


if __name__ == "__main__":
    main()
