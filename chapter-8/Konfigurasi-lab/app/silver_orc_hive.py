"""Latihan 5A: Silver ORC + external table Hive."""
from spark_common import create_spark

SILVER_PARQUET = "hdfs:///datalake/silver/transaksi/"
SILVER_ORC = "hdfs:///datalake/silver/transaksi_orc/"


def main() -> None:
    spark = create_spark("Silver-ORC")

    df = spark.read.parquet(SILVER_PARQUET)
    df.coalesce(2).write.mode("overwrite").orc(SILVER_ORC)

    spark.sql("USE datalake")
    spark.sql("DROP TABLE IF EXISTS transaksi_orc")
    spark.sql(
        f"""
        CREATE EXTERNAL TABLE transaksi_orc (
            id_transaksi STRING,
            id_pelanggan STRING,
            kategori STRING,
            total_nilai DOUBLE,
            kota STRING,
            tanggal_transaksi DATE
        )
        PARTITIONED BY (tahun INT, bulan INT)
        STORED AS ORC
        LOCATION '{SILVER_ORC}'
        """
    )
    spark.sql("MSCK REPAIR TABLE transaksi_orc")
    print("[OK] Tabel datalake.transaksi_orc terdaftar.")
    spark.stop()


if __name__ == "__main__":
    main()
