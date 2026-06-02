"""Query Spark SQL pada Silver — Latihan 5B."""
from spark_common import create_spark


def main() -> None:
    spark = create_spark("SQL-Silver")
    df = spark.read.parquet("hdfs:///datalake/silver/transaksi/")
    df.createOrReplaceTempView("transaksi_silver")

    spark.sql(
        """
        SELECT kategori,
               COUNT(*) AS jumlah,
               ROUND(SUM(total_nilai), 2) AS omzet,
               ROUND(AVG(total_nilai), 2) AS rata_rata
        FROM transaksi_silver
        GROUP BY kategori ORDER BY omzet DESC
        """
    ).show()

    spark.sql(
        """
        SELECT tahun, bulan, COUNT(*) AS n, SUM(total_nilai) AS total
        FROM transaksi_silver
        GROUP BY tahun, bulan ORDER BY tahun, bulan
        """
    ).show()

    spark.stop()


if __name__ == "__main__":
    main()
