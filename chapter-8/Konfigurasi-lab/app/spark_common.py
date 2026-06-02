"""SparkSession dengan Hive support untuk Chapter 8."""
from pyspark.sql import SparkSession


def create_spark(app_name: str, *, hive: bool = True) -> SparkSession:
    builder = (
        SparkSession.builder.appName(app_name)
        .master("yarn")
        .config("spark.sql.shuffle.partitions", "20")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.executor.memory", "512m")
    )
    if hive:
        builder = (
            builder.config("spark.sql.warehouse.dir", "hdfs:///user/hive/warehouse")
            .config("hive.metastore.uris", "thrift://localhost:9083")
            .enableHiveSupport()
        )
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark
