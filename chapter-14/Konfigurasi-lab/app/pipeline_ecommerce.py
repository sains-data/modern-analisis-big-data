"""Pipeline Silver → Gold (e-commerce) — Bab 14 §14.2.2 (tanpa landing JSON)."""
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from spark_common import create_spark

SILVER = "hdfs:///datalake/silver/transaksi/"


def main() -> None:
    spark = create_spark("ECommerce-Pipeline")

    df_silver = (
        spark.read.parquet(SILVER)
        .dropDuplicates(["id_transaksi"])
        .filter(
            F.col("total_nilai").isNotNull()
            & (F.col("total_nilai") > 0)
            & F.col("id_pelanggan").isNotNull()
        )
        .withColumn("total_nilai", F.col("total_nilai").cast("double"))
        .withColumn(
            "tanggal",
            F.coalesce(
                F.col("tanggal_transaksi"),
                F.to_date(F.col("tanggal"), "yyyy-MM-dd"),
            ),
        )
        .withColumn(
            "segmen_nilai",
            F.when(F.col("total_nilai") < 100_000, "rendah")
            .when(F.col("total_nilai") < 1_000_000, "menengah")
            .otherwise("tinggi"),
        )
    )

    print(f"[Silver] {df_silver.count():,} baris valid")

    w_global = Window.partitionBy()
    w_time = Window.orderBy("tahun", "bulan")

    df_tren = (
        df_silver.groupBy("tahun", "bulan")
        .agg(
            F.sum("total_nilai").alias("omzet"),
            F.count("*").alias("n_transaksi"),
            F.countDistinct("id_pelanggan").alias("pelanggan_aktif"),
            F.avg("total_nilai").alias("avg_nilai"),
        )
        .withColumn(
            "periode",
            F.concat(
                F.col("tahun").cast("string"),
                F.lit("-"),
                F.lpad(F.col("bulan").cast("string"), 2, "0"),
            ),
        )
        .withColumn("ma3_omzet", F.avg("omzet").over(w_time.rowsBetween(-2, 0)))
        .withColumn(
            "mom_growth",
            F.round(
                (F.col("omzet") - F.lag("omzet", 1).over(w_time))
                / F.lag("omzet", 1).over(w_time)
                * 100,
                2,
            ),
        )
        .orderBy("tahun", "bulan")
    )

    df_kat = (
        df_silver.groupBy("kategori")
        .agg(
            F.sum("total_nilai").alias("omzet_total"),
            F.count("*").alias("n_transaksi"),
            F.avg("total_nilai").alias("avg_nilai"),
        )
        .withColumn(
            "persen_omzet",
            F.round(F.col("omzet_total") / F.sum("omzet_total").over(w_global) * 100, 2),
        )
        .orderBy(F.col("omzet_total").desc())
    )

    df_rfm = (
        df_silver.groupBy("id_pelanggan")
        .agg(
            F.count("*").alias("frekuensi"),
            F.sum("total_nilai").alias("monetary"),
            F.max("tanggal").alias("last_purchase"),
        )
        .withColumn("recency_hari", F.datediff(F.current_date(), F.col("last_purchase")))
        .withColumn(
            "segmen_rfm",
            F.when(
                (F.col("frekuensi") >= 10) & (F.col("monetary") >= 5_000_000),
                "Champion",
            )
            .when(
                (F.col("frekuensi") >= 5) & (F.col("recency_hari") <= 30),
                "Loyal",
            )
            .when(F.col("recency_hari") > 90, "At Risk")
            .otherwise("Regular"),
        )
    )

    df_kota = (
        df_silver.groupBy("kota")
        .agg(
            F.sum("total_nilai").alias("omzet"),
            F.count("*").alias("transaksi"),
            F.countDistinct("id_pelanggan").alias("pelanggan_unik"),
        )
        .orderBy(F.col("omzet").desc())
    )

    for nama, df in [
        ("tren_bulanan", df_tren),
        ("omzet_kategori", df_kat),
        ("segmentasi_rfm", df_rfm),
        ("omzet_kota", df_kota),
    ]:
        path = f"hdfs:///datalake/gold/{nama}/"
        df.write.mode("overwrite").parquet(path)
        print(f"[Gold] {nama}: {df.count():,} baris → {path}")

    df_tren.select("periode", "omzet", "n_transaksi", "ma3_omzet", "mom_growth").show(12)

    spark.stop()


if __name__ == "__main__":
    main()
