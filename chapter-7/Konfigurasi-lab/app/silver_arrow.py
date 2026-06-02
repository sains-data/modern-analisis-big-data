"""Silver: transformasi & join dengan DuckDB (zero-copy register)."""
import json
import time
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.dataset as ds

from paths import BRONZE_TRX, DATA_PLG_CSV, SILVER_TRX


def log(tahap: str, metrik: dict) -> None:
    print(
        f"[LOG] {json.dumps({'tahap': tahap, 'ts': time.strftime('%H:%M:%S'), **metrik}, ensure_ascii=False)}"
    )


def main() -> None:
    con = duckdb.connect()

    trx_bronze = con.execute(
        f"SELECT * FROM read_parquet('{BRONZE_TRX}/*.parquet')"
    ).arrow()
    log("silver_read_bronze", {"baris": trx_bronze.num_rows})

    plg = con.execute(
        f"SELECT * FROM read_csv_auto('{DATA_PLG_CSV}')"
    ).arrow()
    log("silver_read_pelanggan", {"baris": plg.num_rows})

    con.register("bronze_trx", trx_bronze)
    con.register("pelanggan", plg)

    tabel_silver = con.execute(
        """
        SELECT
            t.id_transaksi,
            t.id_pelanggan,
            p.nama                               AS nama_pelanggan,
            p.segmen,
            TRY_CAST(t.tanggal AS DATE)          AS tanggal,
            YEAR(TRY_CAST(t.tanggal AS DATE))    AS tahun,
            MONTH(TRY_CAST(t.tanggal AS DATE))   AS bulan,
            LOWER(TRIM(t.kategori))              AS kategori,
            INITCAP(TRIM(t.kota))                AS kota,
            TRIM(t.produk)                        AS produk,
            t.jumlah,
            t.kuantitas,
            ROUND(t.jumlah * t.kuantitas, 2)     AS total_nilai,
            current_timestamp                    AS waktu_transform
        FROM bronze_trx t
        INNER JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        WHERE
            t.id_transaksi IS NOT NULL
            AND t.id_pelanggan IS NOT NULL
            AND t.jumlah > 0
            AND t.kuantitas > 0
            AND TRY_CAST(t.tanggal AS DATE) IS NOT NULL
        """
    ).arrow()

    n_silver = tabel_silver.num_rows
    n_bronze = trx_bronze.num_rows
    log(
        "silver_transform",
        {
            "baris_bronze": n_bronze,
            "baris_silver": n_silver,
            "ditolak": n_bronze - n_silver,
            "pct_valid": round(n_silver / max(n_bronze, 1) * 100, 2),
        },
    )

    SILVER_TRX.mkdir(parents=True, exist_ok=True)
    ds.write_dataset(
        tabel_silver,
        base_dir=str(SILVER_TRX),
        format="parquet",
        partitioning=ds.partitioning(
            pa.schema([("tahun", pa.int32()), ("bulan", pa.int32())]),
            flavor="hive",
        ),
        existing_data_behavior="overwrite_or_ignore",
    )
    log("silver_write", {"path": str(SILVER_TRX)})


if __name__ == "__main__":
    main()
