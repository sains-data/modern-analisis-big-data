"""Bronze: ingest CSV ke Parquet dengan PyArrow."""
import datetime
import json
import time
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pcsv
import pyarrow.parquet as pq

from paths import BRONZE_BATCH, BRONZE_TRX, DATA_TRX_CSV


def log(tahap: str, metrik: dict) -> None:
    print(
        f"[LOG] {json.dumps({'tahap': tahap, 'ts': time.strftime('%H:%M:%S'), **metrik}, ensure_ascii=False)}"
    )


def _rename_agg_columns(table: pa.Table) -> pa.Table:
    names = []
    for name in table.schema.names:
        for suffix in ("_one", "_first"):
            if name.endswith(suffix):
                name = name[: -len(suffix)]
                break
        names.append(name)
    return table.rename_columns(names)


def main() -> None:
    opts_konversi = pcsv.ConvertOptions(
        column_types={
            "id_transaksi": pa.string(),
            "id_pelanggan": pa.string(),
            "jumlah": pa.float64(),
            "kuantitas": pa.int32(),
        },
        null_values=["", "NA", "null", "NULL"],
    )
    opts_baca = pcsv.ReadOptions(block_size=1024 * 1024 * 64)

    tabel_raw = pcsv.read_csv(
        str(DATA_TRX_CSV),
        convert_options=opts_konversi,
        read_options=opts_baca,
    )
    log("bronze_read", {"baris": tabel_raw.num_rows, "kolom": tabel_raw.num_columns})

    null_per_kolom = {
        col: pc.sum(pc.is_null(tabel_raw.column(col))).as_py()
        for col in tabel_raw.schema.names
    }
    log("null_check", null_per_kolom)

    n_sebelum = tabel_raw.num_rows
    tabel_dedup = tabel_raw.group_by("id_transaksi").aggregate(
        [
            ("id_pelanggan", "one"),
            ("tanggal", "one"),
            ("kategori", "one"),
            ("produk", "one"),
            ("jumlah", "one"),
            ("kuantitas", "one"),
            ("kota", "one"),
        ]
    )
    tabel_dedup = _rename_agg_columns(tabel_dedup)
    log(
        "dedup",
        {
            "sebelum": n_sebelum,
            "sesudah": tabel_dedup.num_rows,
            "duplikat_dihapus": n_sebelum - tabel_dedup.num_rows,
        },
    )

    tabel_bronze = tabel_dedup.append_column(
        "waktu_ingest",
        pa.array(
            [datetime.datetime.now()] * tabel_dedup.num_rows,
            type=pa.timestamp("ms"),
        ),
    )

    BRONZE_TRX.mkdir(parents=True, exist_ok=True)
    pq.write_table(
        tabel_bronze,
        str(BRONZE_BATCH),
        compression="snappy",
        write_statistics=True,
    )
    log("bronze_write", {"path": str(BRONZE_BATCH), "ukuran": BRONZE_BATCH.stat().st_size})


if __name__ == "__main__":
    main()
