from pyspark.sql import SparkSession, functions as F
from pyspark.ml import PipelineModel

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Inference-M9") \
        .master("yarn") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # ── Muat model dari HDFS ──────────────────────────────────
    print("[1/3] Memuat model dari HDFS...")
    model = PipelineModel.load("hdfs:///models/segmentasi_dt/v1")
    print(f"      Jumlah stage dalam pipeline : {len(model.stages)}")
    for i, stage in enumerate(model.stages):
        print(f"      Stage {i}: {type(stage).__name__}")

    # ── Baca data baru (simulasi: 200 baris dari Silver) ─────
    print("\n[2/3] Membaca data baru untuk inference...")
    df_baru = spark.read.parquet(
        "hdfs:///datalake/silver/transaksi/"
    ).limit(200)
    print(f"      Baris data baru : {df_baru.count()}")

    # ── Jalankan inference ────────────────────────────────────
    # Tambah kolom segmen (diperlukan pipeline karena ada StringIndexer label)
    df_baru = df_baru.withColumn(
        "segmen",
        F.when(F.col("total_nilai") < 100_000, "rendah")
         .when(F.col("total_nilai") < 1_000_000, "menengah")
         .otherwise("tinggi")
    )

    print("\n[3/3] Menjalankan prediksi...")
    df_hasil = model.transform(df_baru)

    print(f"\n      Total diprediksi : {df_hasil.count()}")
    print("\n[Distribusi prediksi]")
    df_hasil.groupBy(
        F.col("prediction").cast("integer").alias("pred_idx")
    ).count().orderBy("pred_idx").show()

    print("\n[Sampel hasil prediksi]")
    df_hasil.select(
        "id_transaksi", "kategori",
        F.round("total_nilai", 0).alias("total_nilai"),
        "segmen",
        F.col("prediction").cast("integer").alias("prediksi")
    ).show(10)

    spark.stop()
