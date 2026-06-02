"""Ekspor Gold Parquet → PostgreSQL untuk Superset — Bab 14 Tahap 3."""
import os

from pyspark.sql import SparkSession

JDBC_URL = os.environ.get(
    "PG_JDBC_URL",
    "jdbc:postgresql://host.docker.internal:5432/analytics",
)
PROPS = {
    "driver": "org.postgresql.Driver",
    "user": os.environ.get("PG_USER", "superset"),
    "password": os.environ.get("PG_PASSWORD", "superset"),
}

TABEL_PETA = {
    "tren_bulanan": "hdfs:///datalake/gold/tren_bulanan/",
    "omzet_kategori": "hdfs:///datalake/gold/omzet_kategori/",
    "omzet_kota": "hdfs:///datalake/gold/omzet_kota/",
    "segmentasi_rfm": "hdfs:///datalake/gold/segmentasi_rfm/",
}


def main() -> None:
    spark = (
        SparkSession.builder.appName("Ekspor-Ch14")
        .master("yarn")
        .config("spark.jars", "/opt/spark/jars/postgresql-42.7.3.jar")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    print(f"[INFO] JDBC URL: {JDBC_URL}")

    for nama_tabel, path in TABEL_PETA.items():
        df = spark.read.parquet(path)
        df.write.jdbc(
            url=JDBC_URL,
            table=nama_tabel,
            mode="overwrite",
            properties=PROPS,
        )
        print(f"[OK] {nama_tabel}: {df.count():,} baris → PostgreSQL")

    spark.stop()


if __name__ == "__main__":
    main()
