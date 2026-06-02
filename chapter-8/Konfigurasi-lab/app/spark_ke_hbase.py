"""Agregasi Silver → profil pelanggan di HBase (happybase)."""
from pyspark.sql import functions as F

from spark_common import create_spark

SILVER = "hdfs:///datalake/silver/transaksi/"
HBASE_HOST = "localhost"
HBASE_PORT = 9090


def main() -> None:
    try:
        import happybase
    except ImportError as exc:
        raise SystemExit(
            "happybase belum terpasang di kontainer. Jalankan: bash scripts/install_happybase.sh"
        ) from exc

    spark = create_spark("Spark-to-HBase", hive=False)
    spark.conf.set("spark.sql.shuffle.partitions", "10")

    ringkasan = (
        spark.read.parquet(SILVER)
        .groupBy("id_pelanggan")
        .agg(
            F.sum("total_nilai").alias("omzet"),
            F.count("*").alias("n_trx"),
            F.max("tanggal_transaksi").alias("tgl_terakhir"),
        )
        .collect()
    )
    spark.stop()

    conn = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
    conn.open()
    if b"profil_pelanggan" not in conn.tables():
        conn.create_table("profil_pelanggan", {"cf": {}, "stats": {}})
    tabel = conn.table("profil_pelanggan")

    with tabel.batch(batch_size=100) as batch:
        for row in ringkasan:
            key = row["id_pelanggan"].encode()
            batch.put(
                key,
                {
                    b"stats:omzet": str(round(float(row["omzet"]), 2)).encode(),
                    b"stats:n_trx": str(row["n_trx"]).encode(),
                    b"stats:tgl_terakhir": str(row["tgl_terakhir"]).encode(),
                },
            )

    print(f"[HBase] {len(ringkasan)} profil ditulis ke profil_pelanggan.")

    for key, data in list(tabel.scan())[:3]:
        print(key.decode(), {k.decode(): v.decode() for k, v in data.items()})

    conn.close()


if __name__ == "__main__":
    main()
