from pyspark.sql import SparkSession, functions as F
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import (
    StringIndexer, VectorAssembler,
    StandardScaler, Imputer
)
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import time

SILVER_TRX  = "hdfs:///datalake/silver/transaksi/"
GOLD_PRED   = "hdfs:///datalake/gold/prediksi_segmen/"
MODEL_PATH  = "hdfs:///models/segmentasi_dt/v1"

def buat_spark():
    return SparkSession.builder \
        .appName("ML-Pipeline-E2E-M9") \
        .master("yarn") \
        .config("spark.sql.shuffle.partitions", "20") \
        .getOrCreate()

def muat_dan_siapkan_data(spark):
    """Baca Silver, buat label segmen, buang null kritis."""
    df = spark.read.parquet(SILVER_TRX)
    df = df.withColumn(
        "segmen",
        F.when(F.col("total_nilai") < 100_000, "rendah")
         .when(F.col("total_nilai") < 1_000_000, "menengah")
         .otherwise("tinggi")
    )
    return df.dropna(subset=["total_nilai", "kuantitas", "harga_satuan"])

def bangun_pipeline():
    """Bangun Pipeline Spark ML lengkap."""
    # Isi null kolom diskon dengan median
    imputer = Imputer(
        inputCols=["diskon"],
        outputCols=["diskon_imp"],
        strategy="median"
    )
    # Encode kolom kategorikal
    kat_idx = StringIndexer(
        inputCol="kategori", outputCol="kat_idx",
        handleInvalid="keep"
    )
    ch_idx = StringIndexer(
        inputCol="channel", outputCol="ch_idx",
        handleInvalid="keep"
    )
    label_idx = StringIndexer(
        inputCol="segmen", outputCol="label",
        handleInvalid="keep"
    )
    # Rakit fitur
    assembler = VectorAssembler(
        inputCols=["kuantitas", "harga_satuan",
                   "diskon_imp", "berat_kg",
                   "kat_idx", "ch_idx"],
        outputCol="features_raw"
    )
    scaler = StandardScaler(
        inputCol="features_raw", outputCol="features",
        withMean=True, withStd=True
    )
    # Model
    dt = DecisionTreeClassifier(
        featuresCol="features",
        labelCol="label",
        maxDepth=6,
        minInstancesPerNode=5,
        impurity="gini"
    )
    return Pipeline(stages=[
        imputer, kat_idx, ch_idx, label_idx,
        assembler, scaler, dt
    ])

def evaluasi_dan_cetak(df_pred, nama_split):
    """Evaluasi dan cetak metrik klasifikasi."""
    mc = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction"
    )
    metrics = {
        "accuracy":  mc.setMetricName("accuracy").evaluate(df_pred),
        "f1":        mc.setMetricName("f1").evaluate(df_pred),
        "precision": mc.setMetricName("weightedPrecision").evaluate(df_pred),
        "recall":    mc.setMetricName("weightedRecall").evaluate(df_pred),
    }
    print(f"\n  [{nama_split}]")
    for nama, nilai in metrics.items():
        print(f"    {nama:<12}: {nilai:.4f}")
    return metrics

if __name__ == "__main__":
    spark = buat_spark()
    spark.sparkContext.setLogLevel("WARN")
    t_total = time.time()

    # ── [1/5] Muat dan siapkan data ──────────────────────
    print("\n" + "="*55)
    print(" [1/5] MEMUAT DATA")
    print("="*55)
    df = muat_dan_siapkan_data(spark)
    n_total = df.count()
    print(f"  Total baris setelah filter null : {n_total:,}")
    df_train, df_test = df.randomSplit([0.8, 0.2], seed=42)
    n_train = df_train.count()
    n_test  = df_test.count()
    print(f"  Train : {n_train:,} baris")
    print(f"  Test  : {n_test:,} baris")

    # ── [2/5] Latih pipeline ─────────────────────────────
    print("\n" + "="*55)
    print(" [2/5] MELATIH PIPELINE")
    print("="*55)
    df_train.cache()
    pipeline = bangun_pipeline()

    t0 = time.time()
    model = pipeline.fit(df_train)
    durasi_train = round(time.time() - t0, 1)
    df_train.unpersist()
    print(f"  Durasi training : {durasi_train}s")

    # ── [3/5] Evaluasi ───────────────────────────────────
    print("\n" + "="*55)
    print(" [3/5] EVALUASI MODEL")
    print("="*55)
    df_pred_train = model.transform(df_train)
    df_pred_test  = model.transform(df_test)
    m_train = evaluasi_dan_cetak(df_pred_train, "Training Set")
    m_test  = evaluasi_dan_cetak(df_pred_test,  "Test Set")

    # Selisih accuracy training vs test (deteksi overfitting)
    gap = m_train["accuracy"] - m_test["accuracy"]
    print(f"\n  Gap accuracy (train-test) : {gap:.4f}")
    if gap > 0.05:
        print("  ⚠ Potensi overfitting terdeteksi (gap > 0.05)")
    else:
        print("  ✓ Generalisasi baik (gap ≤ 0.05)")

    # ── [4/5] Simpan model ───────────────────────────────
    print("\n" + "="*55)
    print(" [4/5] MENYIMPAN MODEL KE HDFS")
    print("="*55)
    model.write().overwrite().save(MODEL_PATH)
    print(f"  Model disimpan  : {MODEL_PATH}")

    # ── [5/5] Simpan prediksi ke Gold ───────────────────
    print("\n" + "="*55)
    print(" [5/5] MENYIMPAN PREDIKSI KE GOLD LAYER")
    print("="*55)
    df_pred_test.select(
        "id_transaksi", "segmen",
        F.col("prediction").cast("integer").alias("pred_idx"),
        F.current_timestamp().alias("inference_time")
    ).write.mode("overwrite").parquet(GOLD_PRED)
    print(f"  Prediksi disimpan : {GOLD_PRED}")

    durasi_total = round(time.time() - t_total, 1)
    print(f"\n{'='*55}")
    print(f" Pipeline selesai dalam {durasi_total}s total")
    print(f"{'='*55}")

    spark.stop()
