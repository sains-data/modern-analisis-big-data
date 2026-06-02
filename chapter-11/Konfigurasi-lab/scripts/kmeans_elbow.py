from pyspark.sql import SparkSession, functions as F
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
import time

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("KMeans-Elbow-M9") \
        .master("yarn") \
        .config("spark.sql.shuffle.partitions", "20") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    df_raw = spark.read.parquet(
        "hdfs:///datalake/silver/transaksi/"
    )

    # ── Agregasi per pelanggan ──────────────────────────────
    df_pel = df_raw.groupBy("id_pelanggan").agg(
        F.count("*").alias("total_trx"),
        F.sum("total_nilai").alias("total_belanja"),
        F.avg("total_nilai").alias("avg_belanja"),
        F.max("total_nilai").alias("maks_belanja"),
        F.countDistinct("kategori").alias("ragam_kategori")
    )
    df_pel.cache()
    n_pelanggan = df_pel.count()
    print(f"\nJumlah pelanggan untuk clustering: {n_pelanggan}")

    # ── Preprocessing: rakit fitur + standarisasi ───────────
    assembler = VectorAssembler(
        inputCols=["total_trx", "total_belanja",
                   "avg_belanja", "maks_belanja",
                   "ragam_kategori"],
        outputCol="features_raw"
    )
    scaler = StandardScaler(
        inputCol="features_raw", outputCol="features",
        withMean=True, withStd=True
    )

    df_assembled = assembler.transform(df_pel)
    scaler_model = scaler.fit(df_assembled)
    df_feat = scaler_model.transform(df_assembled)
    df_feat.cache()

    # ── Elbow Method: K = 2 sampai 7 ───────────────────────
    evaluator = ClusteringEvaluator(
        featuresCol="features",
        metricName="silhouette"
    )

    print(f"\n{'='*55}")
    print(f" ELBOW METHOD — Silhouette Score dan Inertia")
    print(f"{'='*55}")
    print(f"{'K':>3} | {'Silhouette':>12} | {'Inertia':>15} | {'Detik':>7}")
    print(f"{'-'*55}")

    hasil_elbow = []
    best_k, best_sil = 2, -1.0

    for k in range(2, 8):
        t0 = time.time()
        km = KMeans(
            featuresCol="features",
            k=k, maxIter=20, seed=42,
            initMode="k-means||"
        )
        km_model = km.fit(df_feat)
        df_pred  = km_model.transform(df_feat)

        sil     = evaluator.evaluate(df_pred)
        inertia = km_model.summary.trainingCost
        durasi  = round(time.time() - t0, 1)

        hasil_elbow.append({
            "k": k, "silhouette": sil,
            "inertia": inertia, "durasi": durasi
        })

        if sil > best_sil:
            best_sil = sil
            best_k   = k

        print(f"{k:>3} | {sil:>12.4f} | {inertia:>15.2f} | {durasi:>6.1f}s")

    print(f"{'='*55}")
    print(f"\n=> K optimal (silhouette tertinggi): K = {best_k}"
          f" (silhouette = {best_sil:.4f})")

    # ── Latih ulang dengan K optimal ───────────────────────
    print(f"\n[Melatih ulang dengan K={best_k}...]")
    km_final = KMeans(
        featuresCol="features",
        k=best_k, maxIter=20, seed=42,
        initMode="k-means||"
    )
    model_final   = km_final.fit(df_feat)
    df_clustered  = model_final.transform(df_feat)

    # ── Profil tiap klaster ────────────────────────────────
    print(f"\n[Profil Klaster (K={best_k})]")
    df_profile = df_clustered.join(
        df_pel, on="id_pelanggan"
    ).groupBy("prediction").agg(
        F.count("*").alias("n_pelanggan"),
        F.round(F.avg("total_trx"), 1).alias("avg_trx"),
        F.round(F.avg("total_belanja"), 0).alias("avg_total_belanja"),
        F.round(F.avg("avg_belanja"), 0).alias("avg_nilai_per_trx"),
        F.round(F.avg("maks_belanja"), 0).alias("avg_maks_belanja"),
        F.round(F.avg("ragam_kategori"), 2).alias("avg_ragam_kat")
    ).orderBy("prediction")

    df_profile.show(truncate=False)

    # ── Centroid tiap klaster ──────────────────────────────
    print("\n[Centroid Klaster (dalam skala standar)]")
    feat_names = ["total_trx","total_belanja","avg_belanja",
                  "maks_belanja","ragam_kategori"]
    for i, center in enumerate(model_final.clusterCenters()):
        print(f"\n  Klaster {i}:")
        for fname, val in zip(feat_names, center):
            print(f"    {fname:<20}: {val:>8.4f}")

    # ── Simpan ke Gold layer ───────────────────────────────
    df_clustered.select(
        "id_pelanggan",
        F.col("prediction").alias("klaster"),
        "total_trx", "total_belanja",
        "avg_belanja", "maks_belanja", "ragam_kategori"
    ).write.mode("overwrite").parquet(
        "hdfs:///datalake/gold/segmentasi_pelanggan/"
    )
    print("\n[OK] Hasil segmentasi disimpan ke Gold layer.")

    df_pel.unpersist()
    df_feat.unpersist()
    spark.stop()
