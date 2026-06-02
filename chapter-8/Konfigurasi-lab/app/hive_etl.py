"""ETL Bronze → Silver + registrasi external table Hive."""
from pyspark.sql import functions as F

from spark_common import create_spark

BRONZE = "hdfs:///datalake/bronze/transaksi/"
SILVER = "hdfs:///datalake/silver/transaksi/"


def main() -> None:
    spark = create_spark("Hive-ETL")

    df_trx = spark.read.option("header", "true").option("inferSchema", "true").csv(BRONZE)

    df_silver = (
        df_trx.dropDuplicates(["id_transaksi"])
        .withColumn("total_nilai", F.col("total_nilai").cast("double"))
        .withColumn("tanggal_transaksi", F.to_date("tanggal", "yyyy-MM-dd"))
        .withColumn("tahun", F.year("tanggal_transaksi"))
        .withColumn("bulan", F.month("tanggal_transaksi"))
        .filter(F.col("total_nilai").isNotNull() & (F.col("total_nilai") > 0))
        .drop("tanggal")
    )

    df_silver.coalesce(4).write.mode("overwrite").partitionBy("tahun", "bulan").parquet(
        SILVER
    )
    print(f"[Silver] {df_silver.count()} baris")

    spark.sql("CREATE DATABASE IF NOT EXISTS datalake")
    spark.sql("USE datalake")
    spark.sql("DROP TABLE IF EXISTS transaksi")
    spark.sql(
        """
        CREATE EXTERNAL TABLE transaksi (
            id_transaksi      STRING,
            id_pelanggan      STRING,
            kategori          STRING,
            total_nilai       DOUBLE,
            kota              STRING,
            tanggal_transaksi DATE
        )
        PARTITIONED BY (tahun INT, bulan INT)
        STORED AS PARQUET
        LOCATION 'hdfs:///datalake/silver/transaksi/'
        """
    )
    spark.sql("MSCK REPAIR TABLE transaksi")
    print("[Hive] Tabel 'datalake.transaksi' terdaftar.")

    spark.sql(
        """
        SELECT tahun, bulan, COUNT(*) AS n
        FROM transaksi GROUP BY tahun, bulan
        ORDER BY tahun, bulan
        """
    ).show()

    spark.stop()


if __name__ == "__main__":
    main()
