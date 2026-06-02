"""Benchmark ukuran & waktu baca CSV vs Parquet vs ORC."""
import subprocess
import time

from pyspark.sql import functions as F

from spark_common import create_spark

SILVER = "hdfs:///datalake/silver/transaksi/"
BASE = "hdfs:///datalake/benchmark"


def ukuran(path: str) -> str:
    r = subprocess.run(
        ["hdfs", "dfs", "-du", "-s", "-h", path],
        capture_output=True,
        text=True,
    )
    return r.stdout.split()[0] if r.stdout.strip() else "N/A"


def main() -> None:
    spark = create_spark("FormatBenchmark", hive=False)
    spark.conf.set("spark.sql.shuffle.partitions", "10")

    df = spark.read.parquet(SILVER)

    df.coalesce(2).write.mode("overwrite").option("header", "true").csv(f"{BASE}/csv/")
    df.coalesce(2).write.mode("overwrite").option("compression", "snappy").parquet(
        f"{BASE}/parquet/"
    )
    df.coalesce(2).write.mode("overwrite").orc(f"{BASE}/orc/")

    def waktu_baca(path: str, fmt: str) -> float:
        t0 = time.time()
        if fmt == "csv":
            d = spark.read.option("header", "true").csv(path)
        elif fmt == "parquet":
            d = spark.read.parquet(path)
        else:
            d = spark.read.orc(path)
        d.agg(F.sum("total_nilai")).collect()
        return round(time.time() - t0, 2)

    print(f"\n{'Format':<10} {'Ukuran HDFS':>12} {'Waktu (s)':>10}")
    print("-" * 36)
    for fmt, path in [
        ("CSV", f"{BASE}/csv/"),
        ("Parquet", f"{BASE}/parquet/"),
        ("ORC", f"{BASE}/orc/"),
    ]:
        print(f"{fmt:<10} {ukuran(path):>12} {waktu_baca(path, fmt.lower()):>10}")

    spark.stop()


if __name__ == "__main__":
    main()
