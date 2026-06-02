"""Analisis nilai mahasiswa dengan DataFrame API — Latihan 3."""
import os

from pyspark.sql import SparkSession, functions as F

HDFS_WORK = os.environ.get("HDFS_WORK_DIR", "/user/lab/modul5")


def main():
    spark = (
        SparkSession.builder.appName("AnalisisNilai-DataFrame")
        .master("yarn")
        .config("spark.executor.memory", "512m")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    user = sc.sparkUser()
    base = HDFS_WORK if HDFS_WORK.startswith("/user/") else f"/user/{user}/modul5"
    hdfs_path = f"hdfs://{base}/mahasiswa.csv"
    output = f"hdfs://{base}/hasil_nilai"

    df = (
        spark.read.option("header", "true")
        .option("inferSchema", "true")
        .csv(hdfs_path)
    )

    df_nilai = (
        df.withColumn(
            "nilai_akhir",
            F.round(
                df["nilai_uts"] * 0.30
                + df["nilai_uas"] * 0.40
                + df["nilai_tugas"] * 0.30,
                2,
            ),
        )
        .withColumn(
            "grade",
            F.when(F.col("nilai_akhir") >= 85, "A")
            .when(F.col("nilai_akhir") >= 75, "B")
            .when(F.col("nilai_akhir") >= 65, "C")
            .when(F.col("nilai_akhir") >= 55, "D")
            .otherwise("E"),
        )
    )

    print("=== NILAI AKHIR DAN GRADE ===")
    df_nilai.select("nim", "nama", "nilai_akhir", "grade").orderBy(
        F.col("nilai_akhir").desc()
    ).show()

    print("=== DISTRIBUSI GRADE ===")
    df_nilai.groupBy("grade").agg(F.count("*").alias("jumlah")).orderBy("grade").show()

    df_nilai.createOrReplaceTempView("nilai_mahasiswa")
    print("=== HASIL QUERY SQL ===")
    spark.sql(
        """
        SELECT grade,
               COUNT(*) AS jumlah,
               ROUND(AVG(nilai_akhir), 2) AS rata_rata
        FROM nilai_mahasiswa
        GROUP BY grade ORDER BY grade
        """
    ).show()

    df_nilai.write.mode("overwrite").parquet(output)
    print(f"Tersimpan di HDFS: {output}")

    spark.stop()


if __name__ == "__main__":
    main()
