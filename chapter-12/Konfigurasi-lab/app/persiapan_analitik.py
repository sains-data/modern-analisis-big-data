"""Tiga tabel agregat Gold dari Silver — Bab 12 §12.3.1."""
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from spark_common import create_spark

SILVER = "hdfs:///datalake/silver/transaksi/"


def main() -> None:
    spark = create_spark("PersiapanDataAnalitik")
    df = spark.read.parquet(SILVER)

    df_tren = (
        df.groupBy("tahun", "bulan")
        .agg(
            F.sum("total_nilai").alias("omzet"),
            F.count("*").alias("jumlah_transaksi"),
            F.avg("total_nilai").alias("rata_transaksi"),
            F.countDistinct("id_pelanggan").alias("pelanggan_aktif"),
        )
        .withColumn(
            "periode",
            F.concat(
                F.col("tahun").cast("string"),
                F.lit("-"),
                F.lpad(F.col("bulan").cast("string"), 2, "0"),
            ),
        )
        .orderBy("tahun", "bulan")
    )

    df_tren.coalesce(1).write.mode("overwrite").option("header", "true").csv(
        "hdfs:///datalake/gold/tren_bulanan/"
    )
    print(f"[OK] Tren bulanan: {df_tren.count()} baris")

    w_global = Window.partitionBy()
    df_kategori = (
        df.groupBy("kategori")
        .agg(
            F.sum("total_nilai").alias("omzet_total"),
            F.count("*").alias("jumlah_transaksi"),
            F.avg("total_nilai").alias("omzet_rata"),
            F.countDistinct("id_pelanggan").alias("pelanggan_unik"),
        )
        .withColumn(
            "persen_omzet",
            F.round(F.col("omzet_total") / F.sum("omzet_total").over(w_global) * 100, 2),
        )
        .orderBy(F.col("omzet_total").desc())
    )

    df_kategori.coalesce(1).write.mode("overwrite").option("header", "true").csv(
        "hdfs:///datalake/gold/omzet_kategori/"
    )
    print(f"[OK] Kategori: {df_kategori.count()} baris")

    df_kota = (
        df.groupBy("kota")
        .agg(
            F.sum("total_nilai").alias("omzet"),
            F.count("*").alias("transaksi"),
            F.countDistinct("id_pelanggan").alias("pelanggan_unik"),
            F.avg("total_nilai").alias("avg_nilai"),
        )
        .orderBy(F.col("omzet").desc())
    )

    df_kota.coalesce(1).write.mode("overwrite").option("header", "true").csv(
        "hdfs:///datalake/gold/omzet_kota/"
    )
    print(f"[OK] Kota: {df_kota.count()} baris")

    spark.stop()


if __name__ == "__main__":
    main()
