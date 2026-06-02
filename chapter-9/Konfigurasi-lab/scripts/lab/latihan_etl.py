import sys
from pyspark.sql import SparkSession, functions as F


def main(tanggal: str):
    spark = (
        SparkSession.builder.appName(f"ETL-Latihan-{tanggal}")
        .master("yarn")
        .config("spark.sql.shuffle.partitions", "10")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    BRONZE = "hdfs:///datalake/bronze/latihan/"
    SILVER = "hdfs:///datalake/silver/latihan/"

    print(f"[ETL] Memproses data tanggal: {tanggal}")

    df = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(BRONZE)
    )

    n_raw = df.count()
    print(f"[ETL] Baris raw    : {n_raw}")

    df_clean = (
        df.filter(F.col("id").isNotNull() & (F.col("id") != ""))
        .filter(F.col("nilai") > 0)
        .withColumn("nilai", F.col("nilai").cast("double"))
        .withColumn("kategori", F.upper(F.trim(F.col("kategori"))))
        .withColumn("tanggal_proses", F.lit(tanggal))
        .dropDuplicates(["id"])
    )

    n_clean = df_clean.count()
    print(f"[ETL] Baris valid  : {n_clean}")
    print(f"[ETL] Baris ditolak: {n_raw - n_clean}")

    df_clean.coalesce(2).write.mode("overwrite").parquet(SILVER)

    print(f"[ETL] Output ditulis ke: {SILVER}")
    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: latihan_etl.py <tanggal YYYY-MM-DD>")
        sys.exit(1)
    main(sys.argv[1])
