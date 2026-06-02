"""Pipeline Silver -> Gold: join, agregasi per kategori & segmen."""
from pyspark.sql import functions as F

from spark_common import create_spark

SILVER = "hdfs:///datalake/silver/transaksi/"
BRONZE_PLG = "hdfs:///datalake/bronze/pelanggan/"
GOLD_KAT = "hdfs:///datalake/gold/per_kategori/"
GOLD_SEG = "hdfs:///datalake/gold/per_segmen/"


def main() -> None:
    spark = create_spark("Silver-ke-Gold")

    df_trx = spark.read.parquet(SILVER)
    df_plg = spark.read.option("header", "true").option("inferSchema", "true").csv(
        BRONZE_PLG
    )

    print(f"Transaksi Silver: {df_trx.count()} baris")
    print(f"Pelanggan: {df_plg.count()} baris")

    df_joined = df_trx.join(
        F.broadcast(df_plg.select("id_pelanggan", "nama", "segmen")),
        on="id_pelanggan",
        how="inner",
    )

    df_orphan = df_trx.join(df_plg, on="id_pelanggan", how="left_anti")
    print(f"\n[Anti Join] Transaksi tanpa pelanggan: {df_orphan.count()}")
    df_orphan.show()

    print("\n[Analisis per Segmen]")
    df_joined.groupBy("segmen").agg(
        F.count("id_transaksi").alias("jumlah"),
        F.round(F.sum("total_nilai"), 2).alias("omzet"),
        F.round(F.avg("total_nilai"), 2).alias("rata_rata"),
    ).orderBy(F.col("omzet").desc()).show()

    df_joined.cache()
    df_joined.count()

    df_gold_kat = (
        df_joined.groupBy("kategori")
        .agg(
            F.count("*").alias("jumlah_transaksi"),
            F.countDistinct("id_pelanggan").alias("pelanggan_unik"),
            F.round(F.sum("total_nilai"), 2).alias("omzet_total"),
            F.round(F.avg("total_nilai"), 2).alias("rata_rata"),
        )
        .orderBy(F.col("omzet_total").desc())
    )

    df_gold_seg = (
        df_joined.filter(F.col("segmen").isNotNull())
        .groupBy("segmen", "tahun", "bulan")
        .agg(
            F.count("*").alias("transaksi"),
            F.round(F.sum("total_nilai"), 2).alias("omzet"),
        )
        .orderBy("tahun", "bulan", F.col("omzet").desc())
    )

    df_gold_kat.coalesce(2).write.mode("overwrite").parquet(GOLD_KAT)
    df_gold_seg.coalesce(2).write.mode("overwrite").parquet(GOLD_SEG)

    print(f"\n[Gold Kategori] {df_gold_kat.count()} baris")
    df_gold_kat.show(truncate=False)

    df_joined.unpersist()
    spark.stop()


if __name__ == "__main__":
    main()
