"""Window function pada data Silver — Latihan 5A."""
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from spark_common import create_spark


def main() -> None:
    spark = create_spark("WindowFunc")
    df = spark.read.parquet("hdfs:///datalake/silver/transaksi/")

    win = Window.partitionBy("kategori").orderBy(F.col("total_nilai").desc())

    df_rank = df.withColumn("peringkat", F.rank().over(win)).withColumn(
        "kumulatif",
        F.sum("total_nilai").over(
            win.rowsBetween(Window.unboundedPreceding, Window.currentRow)
        ),
    )

    df_rank.select("kategori", "id_transaksi", "total_nilai", "peringkat", "kumulatif").filter(
        F.col("peringkat") <= 3
    ).orderBy("kategori", "peringkat").show(truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()
