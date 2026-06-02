"""Generator dataset transaksi Modul 9 ke HDFS Bronze + Silver."""

import random
import uuid

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

KATEGORI = ["elektronik", "fashion", "makanan", "kesehatan", "otomotif", "olahraga"]
CHANNEL = ["mobile", "web", "atm", "teller"]
N = 10_000

if __name__ == "__main__":
    spark = SparkSession.builder.appName("BuatDataML").master("yarn").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    random.seed(42)
    rows = []
    for _ in range(N):
        kat = random.choice(KATEGORI)
        channel = random.choice(CHANNEL)
        kuantitas = random.randint(1, 20)
        base = {
            "elektronik": 500_000,
            "otomotif": 800_000,
            "fashion": 200_000,
            "makanan": 50_000,
            "kesehatan": 150_000,
            "olahraga": 300_000,
        }[kat]
        harga = base * random.uniform(0.5, 3.0)
        diskon = random.uniform(0, 0.3)
        total = kuantitas * harga * (1 - diskon)
        berat = round(random.uniform(0.1, 10.0), 2)
        rows.append(
            (
                str(uuid.uuid4())[:8],
                f"usr-{random.randint(1, 200):04d}",
                kat,
                channel,
                kuantitas,
                round(harga, 2),
                round(diskon, 3),
                round(total, 2),
                berat,
            )
        )

    schema = StructType(
        [
            StructField("id_transaksi", StringType(), True),
            StructField("id_pelanggan", StringType(), True),
            StructField("kategori", StringType(), True),
            StructField("channel", StringType(), True),
            StructField("kuantitas", IntegerType(), True),
            StructField("harga_satuan", DoubleType(), True),
            StructField("diskon", DoubleType(), True),
            StructField("total_nilai", DoubleType(), True),
            StructField("berat_kg", DoubleType(), True),
        ]
    )

    df = spark.createDataFrame(rows, schema=schema)
    df.write.mode("overwrite").parquet("hdfs:///datalake/bronze/transaksi/")
    df.write.mode("overwrite").parquet("hdfs:///datalake/silver/transaksi/")

    print(f"\n[OK] Dataset dibuat: {df.count()} baris")
    df.printSchema()
    df.show(5)
    spark.stop()
