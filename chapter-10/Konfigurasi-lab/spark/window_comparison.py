"""
window_comparison.py
Membandingkan tumbling window dan sliding window secara bersamaan.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, StringType, StructField, StructType, TimestampType

KAFKA_SERVERS = "localhost:9092"
TOPIC_IN = "transaksi-stream"
CHECKPOINT_DIR = "/tmp/checkpoints/exp_a"

schema = StructType(
    [
        StructField("channel", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("event_time", TimestampType(), True),
    ]
)

if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("WindowComparison")
        .master("local[2]")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    df_raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_SERVERS)
        .option("subscribe", TOPIC_IN)
        .option("startingOffsets", "latest")
        .load()
    )

    df = df_raw.select(F.from_json(F.col("value").cast("string"), schema).alias("d")).select("d.*")

    df_tumbling = (
        df.withWatermark("event_time", "3 minutes")
        .groupBy(F.window("event_time", "2 minutes"))
        .agg(F.count("*").alias("jumlah"), F.sum("amount").alias("total_tumbling"))
        .select(
            F.col("window.start").alias("w_start"),
            F.col("window.end").alias("w_end"),
            "jumlah",
            F.round("total_tumbling", 0).alias("total"),
        )
    )

    df_sliding = (
        df.withWatermark("event_time", "3 minutes")
        .groupBy(F.window("event_time", "2 minutes", "1 minute"))
        .agg(F.count("*").alias("jumlah"), F.sum("amount").alias("total_sliding"))
        .select(
            F.col("window.start").alias("w_start"),
            F.col("window.end").alias("w_end"),
            "jumlah",
            F.round("total_sliding", 0).alias("total"),
        )
    )

    df_tumbling.writeStream.queryName("tumbling_2min").outputMode("update").format("console").option(
        "truncate", False
    ).option("checkpointLocation", CHECKPOINT_DIR + "/tumbling").trigger(processingTime="20 seconds").start()

    df_sliding.writeStream.queryName("sliding_2min_1min").outputMode("update").format("console").option(
        "truncate", False
    ).option("checkpointLocation", CHECKPOINT_DIR + "/sliding").trigger(processingTime="20 seconds").start()

    print("\n[WindowComparison] Dua query aktif.")
    print("[WindowComparison] Spark UI: http://localhost:4040")
    print("[WindowComparison] Tekan Ctrl+C untuk berhenti.\n")

    spark.streams.awaitAnyTermination()
