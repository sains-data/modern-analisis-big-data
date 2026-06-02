"""Aproksimasi Pi dengan Monte Carlo (RDD) — Latihan 2 & 5."""
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
        SparkSession.builder.appName("AproksimasiPi-YARN")
        .master("yarn")
        .config("spark.executor.memory", "512m")
        .config("spark.executor.cores", "1")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    print(f"Spark versi: {sc.version} | Master: {sc.master}")
    print(f"Jumlah dart: {jumlah_dart:,} | Slices: {slices}")

    t0 = time.time()
    rdd = sc.parallelize(range(jumlah_dart), slices)
    dart_dalam = rdd.map(lempar_dart).reduce(lambda a, b: a + b)
    elapsed = time.time() - t0

    pi = 4.0 * dart_dalam / jumlah_dart
    print(f"Aproksimasi Pi  : {pi:.6f}")
    print(f"Pi sesungguhnya : 3.141593")
    print(f"Selisih         : {abs(pi - 3.141593):.6f}")
    print(f"Waktu (detik)   : {elapsed:.2f}")

    spark.stop()


if __name__ == "__main__":
    main()
