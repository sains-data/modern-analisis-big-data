from pyspark.sql import SparkSession, functions as F
from pyspark.ml.feature import (
    VectorAssembler, StandardScaler, StringIndexer
)
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("RegParam-Eksplorasi-M9") \
        .master("yarn") \
        .config("spark.sql.shuffle.partitions", "20") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = spark.read.parquet("hdfs:///datalake/silver/transaksi/")

    kat_idx = StringIndexer(
        inputCol="kategori", outputCol="kat_idx",
        handleInvalid="keep"
    )
    ch_idx = StringIndexer(
        inputCol="channel", outputCol="ch_idx",
        handleInvalid="keep"
    )
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

    df_train, df_test = df.randomSplit([0.8, 0.2], seed=42)
    df_train.cache()

    evaluator = RegressionEvaluator(
        labelCol="total_nilai",
        predictionCol="prediction"
    )

    reg_values = [0.0, 0.001, 0.01, 0.1, 1.0, 10.0]

    print(f"\n{'='*60}")
    print(f" EKSPERIMEN REGULARISASI LINEAR REGRESSION")
    print(f"{'='*60}")
    print(f"{'regParam':>10} | {'RMSE Train':>14} | {'RMSE Test':>14} | {'R2 Test':>9}")
    print(f"{'-'*60}")

    for reg in reg_values:
        lr = LinearRegression(
            featuresCol="features",
            labelCol="total_nilai",
            maxIter=100,
            regParam=reg,
            elasticNetParam=0.0
        )
        pipe = Pipeline(stages=[
            kat_idx, ch_idx, assembler, scaler, lr
        ])
        model = pipe.fit(df_train)

        pred_train = model.transform(df_train)
        pred_test  = model.transform(df_test)

        rmse_train = evaluator.setMetricName("rmse").evaluate(pred_train)
        rmse_test  = evaluator.setMetricName("rmse").evaluate(pred_test)
        r2_test    = evaluator.setMetricName("r2").evaluate(pred_test)

        print(f"{reg:>10} | {rmse_train:>14,.0f} | {rmse_test:>14,.0f} | {r2_test:>9.4f}")

    print(f"{'='*60}")
    df_train.unpersist()
    spark.stop()
