"""MA3, MoM growth, kumulatif — Bab 12 §12.3.2."""
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from spark_common import create_spark


def main() -> None:
    spark = create_spark("MetrikLanjutan")

    df_tren = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv("hdfs:///datalake/gold/tren_bulanan/")
    )

    w = Window.orderBy("tahun", "bulan")

    df_ma = df_tren.withColumn("ma3_omzet", F.avg("omzet").over(w.rowsBetween(-2, 0)))

    df_final = (
        df_ma.withColumn("omzet_bulan_lalu", F.lag("omzet", 1).over(w))
        .withColumn(
            "mom_growth_pct",
            F.round(
                (F.col("omzet") - F.col("omzet_bulan_lalu"))
                / F.col("omzet_bulan_lalu")
                * 100,
                2,
            ),
        )
        .withColumn(
            "kumulatif_omzet",
            F.sum("omzet").over(w.rowsBetween(Window.unboundedPreceding, 0)),
        )
        .withColumn("peringkat_omzet", F.rank().over(Window.orderBy(F.col("omzet").desc())))
    )

    df_final.show(12, truncate=False)

    df_final.coalesce(1).write.mode("overwrite").option("header", "true").csv(
        "hdfs:///datalake/gold/tren_lanjutan/"
    )
    print("[OK] Metrik lanjutan → hdfs:///datalake/gold/tren_lanjutan/")
    spark.stop()


if __name__ == "__main__":
    main()
