"""Demonstrasi .cache() pada RDD — Latihan 5 Bagian B."""
import os
import random
import time

from pyspark.sql import SparkSession


def lempar_dart(_):
    x, y = random.random(), random.random()
    return 1 if (x**2 + y**2) <= 1.0 else 0


def main():
    slices = int(os.environ.get("SLICES", "4"))
    jumlah_dart = int(os.environ.get("JUMLAH_DART", "1000000"))

    spark = (
        SparkSession.builder.appName("AproksimasiPi-Cache")
        .master("yarn")
        .config("spark.executor.memory", "512m")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    rdd = sc.parallelize(range(jumlah_dart), slices).cache()

    t0 = time.time()
    dart1 = rdd.map(lempar_dart).reduce(lambda a, b: a + b)
    t1 = time.time() - t0

    t0 = time.time()
    dart2 = rdd.map(lempar_dart).reduce(lambda a, b: a + b)
    t2 = time.time() - t0

    print(f"Run 1 (tanpa cache warm): dart_dalam={dart1}, waktu={t1:.2f}s")
    print(f"Run 2 (dari cache)      : dart_dalam={dart2}, waktu={t2:.2f}s")

    spark.stop()


if __name__ == "__main__":
    main()
