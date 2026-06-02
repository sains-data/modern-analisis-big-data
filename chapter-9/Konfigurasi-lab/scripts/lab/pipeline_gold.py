import sys
from pyspark.sql import SparkSession, functions as F


def main(tanggal: str):
    spark = (
        SparkSession.builder.appName(f"Gold-Latihan-{tanggal}")
        .master("yarn")
        .config("spark.sql.shuffle.partitions", "10")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    SILVER = "hdfs:///datalake/silver/latihan/"
    GOLD = "hdfs:///datalake/gold/latihan/"

    print(f"[GOLD] Agregasi Silver → Gold untuk tanggal: {tanggal}")

    df = spark.read.parquet(SILVER)
    n = df.count()
    print(f"[GOLD] Baris Silver dibaca: {n}")

    df_agg = df.groupBy("kategori", "tanggal_proses").agg(
        F.count("*").alias("jumlah_transaksi"),
        F.sum("nilai").alias("total_nilai"),
        F.avg("nilai").alias("rata_nilai"),
        F.min("nilai").alias("min_nilai"),
        F.max("nilai").alias("max_nilai"),
    )

    df_agg.coalesce(1).write.mode("overwrite").parquet(GOLD)

    print("[GOLD] Agregasi per kategori:")
    df_agg.orderBy(F.col("total_nilai").desc()).show(truncate=False)
    print(f"[GOLD] Output ditulis ke: {GOLD}")
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pipeline_gold.py <tanggal YYYY-MM-DD>")
        sys.exit(1)
    main(sys.argv[1])
