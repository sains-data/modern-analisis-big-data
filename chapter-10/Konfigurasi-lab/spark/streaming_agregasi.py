"""
streaming_agregasi.py
Pipeline Spark Structured Streaming: baca dari Kafka, agregasi window, tulis ke console.

Jalankan dari Konfigurasi-lab/:
  source .venv/bin/activate
  spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
    --master local[2] \
    --conf spark.sql.shuffle.partitions=4 \
    spark/streaming_agregasi.py
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

KAFKA_SERVERS = "localhost:9092"
TOPIC_IN = "transaksi-stream"
CHECKPOINT_DIR = "/tmp/checkpoints/streaming-agregasi"

schema_event = StructType(
    [
        StructField("event_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("product", StringType(), True),
        StructField("channel", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("event_time", TimestampType(), True),
    ]
)

if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("StreamingAgregatWindow")
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
        .option("maxOffsetsPerTrigger", 100)
        .option("failOnDataLoss", "false")
        .load()
    )

    df = (
        df_raw.select(
            F.from_json(F.col("value").cast("string"), schema_event).alias("d"),
            F.col("partition").alias("kafka_partition"),
            F.col("offset").alias("kafka_offset"),
        )
        .select("d.*", "kafka_partition", "kafka_offset")
    )

    df_q1 = (
        df.withWatermark("event_time", "2 minutes")
        .groupBy(F.window("event_time", "1 minute"), "channel")
        .agg(
            F.count("*").alias("jumlah"),
            F.sum("amount").alias("total"),
            F.avg("amount").alias("rata_rata"),
        )
        .select(
            F.col("window.start").alias("window_start"),
            F.col("window.end").alias("window_end"),
            "channel",
            "jumlah",
            F.round("total", 0).alias("total"),
            F.round("rata_rata", 0).alias("rata_rata"),
        )
    )

    df_q2 = (
        df.groupBy("user_id")
        .agg(
            F.count("*").alias("total_transaksi"),
            F.sum("amount").alias("total_amount"),
        )
        .orderBy(F.col("total_amount").desc())
    )

    q1 = (
        df_q1.writeStream.queryName("penjualan_per_channel")
        .outputMode("update")
        .format("console")
        .option("truncate", False)
        .option("numRows", 10)
        .option("checkpointLocation", CHECKPOINT_DIR + "/q1")
        .trigger(processingTime="15 seconds")
        .start()
    )

    q2 = (
        df_q2.writeStream.queryName("top_user")
        .outputMode("complete")
        .format("console")
        .option("truncate", False)
        .option("numRows", 5)
        .option("checkpointLocation", CHECKPOINT_DIR + "/q2")
        .trigger(processingTime="30 seconds")
        .start()
    )

    print("\n[Streaming] Pipeline aktif.")
    print("[Streaming] Spark UI → http://localhost:4040")
    print("[Streaming] Kafka UI → http://localhost:8080")
    print("[Streaming] Tekan Ctrl+C untuk berhenti.\n")

    spark.streams.awaitAnyTermination()
