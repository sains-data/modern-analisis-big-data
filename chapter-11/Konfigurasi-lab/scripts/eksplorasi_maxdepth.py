from pyspark.sql import SparkSession, functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    StringIndexer, VectorAssembler, StandardScaler
)
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("MaxDepth-Eksplorasi-M9") \
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

    kat_idx   = StringIndexer(inputCol="kategori",
                              outputCol="kat_idx", handleInvalid="keep")
    ch_idx    = StringIndexer(inputCol="channel",
                              outputCol="ch_idx",  handleInvalid="keep")
    label_idx = StringIndexer(inputCol="segmen",
                              outputCol="label",   handleInvalid="keep")
    assembler = VectorAssembler(
        inputCols=["kuantitas","harga_satuan","diskon",
                   "berat_kg","kat_idx","ch_idx"],
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

    depth_values = [2, 4, 6, 8, 10]

    print(f"\n{'='*75}")
    print(f" EKSPERIMEN maxDepth DECISION TREE")
    print(f"{'='*75}")
    print(f"{'Depth':>6} | {'Acc Train':>10} | {'Acc Test':>10} "
          f"| {'F1 Test':>9} | {'Gap':>8} | {'Nodes':>7}")
    print(f"{'-'*75}")

    for depth in depth_values:
        dt = DecisionTreeClassifier(
            featuresCol="features", labelCol="label",
            maxDepth=depth, impurity="gini",
            minInstancesPerNode=5
        )
        pipe = Pipeline(stages=[
            kat_idx, ch_idx, label_idx, assembler, scaler, dt
        ])
        model = pipe.fit(df_train)
        dt_model = model.stages[-1]

        pred_train = model.transform(df_train)
        pred_test  = model.transform(df_test)

        acc_train = mc_eval.setMetricName("accuracy").evaluate(pred_train)
        acc_test  = mc_eval.setMetricName("accuracy").evaluate(pred_test)
        f1_test   = mc_eval.setMetricName("f1").evaluate(pred_test)
        gap       = acc_train - acc_test

        print(f"{depth:>6} | {acc_train:>10.4f} | {acc_test:>10.4f} "
              f"| {f1_test:>9.4f} | {gap:>8.4f} | {dt_model.numNodes:>7}")

    print(f"{'='*75}")
    df_train.unpersist()
    spark.stop()
