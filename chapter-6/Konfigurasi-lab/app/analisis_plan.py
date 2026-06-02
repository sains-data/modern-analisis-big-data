"""Analisis execution plan dan benchmark cache."""
import time

from pyspark.sql import functions as F

from spark_common import create_spark

SILVER = "hdfs:///datalake/silver/transaksi/"


def main() -> None:
    spark = create_spark("Analisis-Plan")
    df = spark.read.parquet(SILVER)

    print("=" * 50 + "\nQUERY 1: Filter + Select (Narrow)\n" + "=" * 50)
    df.select("id_transaksi", "kategori", "total_nilai").filter(
        F.col("total_nilai") > 500_000
    ).explain(mode="formatted")

    print("=" * 50 + "\nQUERY 2: GroupBy (Wide)\n" + "=" * 50)
    df.groupBy("kategori").agg(F.sum("total_nilai").alias("omzet")).explain(
        mode="formatted"
    )

    print("=" * 50 + "\nQUERY 3: Broadcast Join\n" + "=" * 50)
    df_plg = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv("hdfs:///datalake/bronze/pelanggan/")
    )
    df.join(
        F.broadcast(df_plg.select("id_pelanggan", "segmen")),
        on="id_pelanggan",
        how="inner",
    ).select("id_transaksi", "segmen", "total_nilai").explain(mode="formatted")

    print("\n[Benchmark Cache]")
    t0 = time.time()
    df.filter(F.col("total_nilai") > 500_000).count()
    df.groupBy("kategori").agg(F.sum("total_nilai")).count()
    df.groupBy("kota").agg(F.count("*")).count()
    print(f"Tanpa cache: {time.time() - t0:.2f} detik")

    df.cache()
    df.count()
    t0 = time.time()
    df.filter(F.col("total_nilai") > 500_000).count()
    df.groupBy("kategori").agg(F.sum("total_nilai")).count()
    df.groupBy("kota").agg(F.count("*")).count()
    print(f"Dengan cache: {time.time() - t0:.2f} detik")
    df.unpersist()

    spark.stop()


if __name__ == "__main__":
    main()
