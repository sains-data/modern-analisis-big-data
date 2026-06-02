from pyspark.sql import SparkSession, functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    StringIndexer, VectorAssembler, StandardScaler
)
from pyspark.ml.classification import (
    LogisticRegression, DecisionTreeClassifier
)
from pyspark.ml.evaluation import (
    MulticlassClassificationEvaluator
)
import time

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("Klasifikasi-M9") \
        .master("yarn") \
        .config("spark.sql.shuffle.partitions", "20") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df = spark.read.parquet(
        "hdfs:///datalake/silver/transaksi/"
    ).withColumn(
        "segmen",
        F.when(F.col("total_nilai") < 100_000, "rendah")
         .when(F.col("total_nilai") < 1_000_000, "menengah")
         .otherwise("tinggi")
    )

    # Preprocessing bersama
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

    mc_eval = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction"
    )

    hasil = {}

    # ── Model 1: Logistic Regression ──────────────────────
    lr = LogisticRegression(
        featuresCol="features", labelCol="label",
        maxIter=100, regParam=0.01,
        family="multinomial"
    )
    pipe_lr = Pipeline(stages=[
        kat_idx, ch_idx, label_idx, assembler, scaler, lr
    ])

    t0 = time.time()
    model_lr = pipe_lr.fit(df_train)
    dur_lr = round(time.time() - t0, 1)

    pred_lr  = model_lr.transform(df_test)
    acc_lr   = mc_eval.setMetricName("accuracy").evaluate(pred_lr)
    f1_lr    = mc_eval.setMetricName("f1").evaluate(pred_lr)
    prec_lr  = mc_eval.setMetricName("weightedPrecision").evaluate(pred_lr)
    rec_lr   = mc_eval.setMetricName("weightedRecall").evaluate(pred_lr)
    hasil["Logistic Regression"] = {
        "accuracy": acc_lr, "f1": f1_lr,
        "precision": prec_lr, "recall": rec_lr,
        "durasi": dur_lr
    }

    # ── Model 2: Decision Tree ─────────────────────────────
    dt = DecisionTreeClassifier(
        featuresCol="features", labelCol="label",
        maxDepth=6, impurity="gini",
        minInstancesPerNode=10
    )
    pipe_dt = Pipeline(stages=[
        kat_idx, ch_idx, label_idx, assembler, scaler, dt
    ])

    t0 = time.time()
    model_dt = pipe_dt.fit(df_train)
    dur_dt = round(time.time() - t0, 1)

    pred_dt  = model_dt.transform(df_test)
    acc_dt   = mc_eval.setMetricName("accuracy").evaluate(pred_dt)
    f1_dt    = mc_eval.setMetricName("f1").evaluate(pred_dt)
    prec_dt  = mc_eval.setMetricName("weightedPrecision").evaluate(pred_dt)
    rec_dt   = mc_eval.setMetricName("weightedRecall").evaluate(pred_dt)
    hasil["Decision Tree"] = {
        "accuracy": acc_dt, "f1": f1_dt,
        "precision": prec_dt, "recall": rec_dt,
        "durasi": dur_dt
    }

    df_train.unpersist()

    # ── Ringkasan perbandingan ─────────────────────────────
    print(f"\n{'='*65}")
    print(f"{'Model':<25} {'Accuracy':>9} {'F1':>9} "
          f"{'Precision':>10} {'Recall':>9} {'Detik':>7}")
    print(f"{'='*65}")
    for nama, m in hasil.items():
        print(f"{nama:<25} {m['accuracy']:>9.4f} {m['f1']:>9.4f} "
              f"{m['precision']:>10.4f} {m['recall']:>9.4f} "
              f"{m['durasi']:>7.1f}s")
    print(f"{'='*65}")

    # ── Confusion matrix Decision Tree ────────────────────
    print("\n[Confusion Matrix — Decision Tree]")
    pred_dt.groupBy("segmen", "prediction") \
           .count() \
           .orderBy("segmen", "prediction") \
           .show()

    # ── Feature importance Decision Tree ──────────────────
    dt_model = model_dt.stages[-1]
    feat_names = ["kuantitas", "harga_satuan", "diskon",
                  "berat_kg", "kat_idx", "ch_idx"]
    print("\n[Feature Importance — Decision Tree]")
    importances = list(zip(feat_names, dt_model.featureImportances))
    for fname, imp in sorted(importances, key=lambda x: -x[1]):
        bar = "█" * int(imp * 50)
        print(f"  {fname:<15}: {imp:.4f}  {bar}")

    print(f"\nKedalaman pohon : {dt_model.depth}")
    print(f"Jumlah node     : {dt_model.numNodes}")

    spark.stop()
