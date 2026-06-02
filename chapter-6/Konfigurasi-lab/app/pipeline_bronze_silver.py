"""Pipeline Bronze -> Silver: validasi, dedup, Parquet terpartisi."""
import json
import time

from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from spark_common import create_spark

BRONZE = "hdfs:///datalake/bronze/transaksi/"
SILVER = "hdfs:///datalake/silver/transaksi/"


def log(tahap: str, metrik: dict) -> None:
    print(
        f"[LOG] {json.dumps({'tahap': tahap, 'ts': time.strftime('%H:%M:%S'), **metrik}, ensure_ascii=False)}"
    )


def main() -> None:
    spark = create_spark("Pipeline-Bronze-Silver")

    skema = StructType(
        [
            StructField("id_transaksi", StringType(), True),
            StructField("id_pelanggan", StringType(), True),
            StructField("tanggal", StringType(), True),
            StructField("kategori", StringType(), True),
            StructField("produk", StringType(), True),
            StructField("jumlah", StringType(), True),
            StructField("kuantitas", StringType(), True),
            StructField("kota", StringType(), True),
        ]
    )
    df_raw = spark.read.schema(skema).option("header", "true").csv(BRONZE)
    n_raw = df_raw.count()
    log("bronze_read", {"baris": n_raw, "partisi": df_raw.rdd.getNumPartitions()})

    print("[Null per kolom]")
    df_raw.select(
        [F.sum(F.col(c).isNull().cast("int")).alias(c) for c in df_raw.columns]
    ).show()

    df_clean = (
        df_raw.dropDuplicates(["id_transaksi"])
        .withColumn("jumlah", F.col("jumlah").cast(DoubleType()))
        .withColumn("kuantitas", F.col("kuantitas").cast(IntegerType()))
        .withColumn("tanggal_transaksi", F.to_date(F.col("tanggal"), "yyyy-MM-dd"))
        .withColumn("kategori", F.lower(F.trim(F.col("kategori"))))
        .withColumn("kota", F.initcap(F.trim(F.col("kota"))))
        .withColumn("produk", F.trim(F.col("produk")))
    )

    df_valid = df_clean.filter(
        F.col("id_transaksi").isNotNull()
        & F.col("id_pelanggan").isNotNull()
        & F.col("tanggal_transaksi").isNotNull()
        & F.col("jumlah").isNotNull()
        & (F.col("jumlah") > 0)
        & (F.col("kuantitas") > 0)
    )
    n_valid = df_valid.count()
    log(
        "validasi",
        {
            "baris_masuk": n_raw,
            "baris_valid": n_valid,
            "baris_ditolak": n_raw - n_valid,
        },
    )

    df_silver = (
        df_valid.withColumn("tahun", F.year("tanggal_transaksi"))
        .withColumn("bulan", F.month("tanggal_transaksi"))
        .withColumn("total_nilai", F.round(F.col("jumlah") * F.col("kuantitas"), 2))
        .withColumn("waktu_ingest", F.current_timestamp())
        .drop("tanggal")
    )

    print("\n[Skema Silver:]")
    df_silver.printSchema()
    df_silver.show(10, truncate=False)

    df_silver.coalesce(2).write.mode("overwrite").partitionBy("tahun", "bulan").parquet(
        SILVER
    )
    log("silver_write", {"path": SILVER})

    df_ver = spark.read.parquet(SILVER)
    print(f"\n[Verifikasi] {df_ver.count()} baris terbaca dari Silver")

    spark.stop()


if __name__ == "__main__":
    main()
