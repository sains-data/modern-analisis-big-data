"""SparkSession untuk pipeline visualisasi Chapter 12."""
from pyspark.sql import SparkSession


def create_spark(app_name: str) -> SparkSession:
    spark = (
        SparkSession.builder.appName(app_name)
        .master("yarn")
        .config("spark.sql.shuffle.partitions", "20")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.executor.memory", "512m")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark
