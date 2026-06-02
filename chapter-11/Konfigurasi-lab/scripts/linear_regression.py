from pyspark.sql import SparkSession, functions as F
from pyspark.ml.feature import (
    VectorAssembler, StringIndexer, StandardScaler
)
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline
import time

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("LinearRegression-M9") \
        .master("yarn") \
        .config("spark.sql.shuffle.partitions", "20") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = spark.read.parquet("hdfs:///datalake/silver/transaksi/")

    # Encode kolom kategorikal
    cat_idx = StringIndexer(
        inputCol="kategori", outputCol="kat_idx",
        handleInvalid="keep"
    )
    ch_idx = StringIndexer(
        inputCol="channel", outputCol="ch_idx",
        handleInvalid="keep"
    )

    # Rakit semua fitur
    assembler = VectorAssembler(
        inputCols=["kuantitas", "harga_satuan",
                   "diskon", "berat_kg",
                   "kat_idx", "ch_idx"],
        outputCol="features_raw"
    )

    scaler = StandardScaler(
        inputCol="features_raw", outputCol="features",
        withMean=True, withStd=True
    )

    lr = LinearRegression(
        featuresCol="features",
        labelCol="total_nilai",
        maxIter=100,
        regParam=0.1,
        elasticNetParam=0.0
    )

    pipeline = Pipeline(
        stages=[cat_idx, ch_idx, assembler, scaler, lr]
    )

    df_train, df_test = df.randomSplit([0.8, 0.2], seed=42)
    df_train.cache()

    t0 = time.time()
    model = pipeline.fit(df_train)
    durasi_train = round(time.time() - t0, 1)
    df_train.unpersist()

    df_pred = model.transform(df_test)

    evaluator = RegressionEvaluator(
        labelCol="total_nilai",
        predictionCol="prediction"
    )

    rmse = evaluator.setMetricName("rmse").evaluate(df_pred)
    mae  = evaluator.setMetricName("mae").evaluate(df_pred)
    r2   = evaluator.setMetricName("r2").evaluate(df_pred)

    print(f"\n{'='*50}")
    print(f" LINEAR REGRESSION — TEST SET")
    print(f"{'='*50}")
    print(f" Durasi training  : {durasi_train}s")
    print(f" RMSE             : {rmse:>15,.2f}")
    print(f" MAE              : {mae:>15,.2f}")
    print(f" R²               : {r2:>15.4f}")
    print(f"{'='*50}")

    # Koefisien model
    lr_model = model.stages[-1]
    feat_names = ["kuantitas", "harga_satuan", "diskon",
                  "berat_kg", "kat_idx", "ch_idx"]
    print("\n[Koefisien Model]")
    for fname, coef in zip(feat_names, lr_model.coefficients):
        print(f"  {fname:<15}: {coef:>15.2f}")
    print(f"  {'intercept':<15}: {lr_model.intercept:>15.2f}")

    # Tampilkan 10 prediksi vs aktual
    print("\n[Sampel Prediksi vs Aktual]")
    df_pred.select(
        F.round("total_nilai", 0).alias("aktual"),
        F.round("prediction", 0).alias("prediksi"),
        F.round(
            F.abs(F.col("total_nilai") - F.col("prediction")), 0
        ).alias("selisih_abs")
    ).show(10)

    spark.stop()
