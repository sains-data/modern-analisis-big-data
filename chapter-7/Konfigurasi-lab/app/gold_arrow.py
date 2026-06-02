"""Gold: agregasi bisnis dengan Polars (lazy scan)."""
import json
import time
from pathlib import Path

import polars as pl
import pyarrow.parquet as pq

from paths import GOLD_DIR, SILVER_TRX


def log(tahap: str, metrik: dict) -> None:
    print(
        f"[LOG] {json.dumps({'tahap': tahap, 'ts': time.strftime('%H:%M:%S'), **metrik}, ensure_ascii=False)}"
    )


def main() -> None:
    silver_glob = str(SILVER_TRX / "**" / "*.parquet")
    lf_silver = pl.scan_parquet(silver_glob, hive_partitioning=True)
    log("gold_read", {"status": "lazy scan", "path": silver_glob})

    lf_gold_kat = (
        lf_silver.group_by("kategori")
        .agg(
            pl.len().alias("jumlah_transaksi"),
            pl.col("id_pelanggan").n_unique().alias("pelanggan_unik"),
            pl.col("total_nilai").sum().round(2).alias("omzet_total"),
            pl.col("total_nilai").mean().round(2).alias("rata_rata_transaksi"),
            pl.col("total_nilai").max().alias("transaksi_terbesar"),
        )
        .sort("omzet_total", descending=True)
    )

    lf_gold_seg = (
        lf_silver.group_by(["segmen", "tahun", "bulan"])
        .agg(
            pl.len().alias("n_transaksi"),
            pl.col("total_nilai").sum().round(2).alias("omzet"),
            pl.col("id_pelanggan").n_unique().alias("pelanggan_aktif"),
        )
        .sort(["tahun", "bulan", "omzet"], descending=[False, False, True])
    )

    lf_gold_top = (
        lf_silver.with_columns(
            pl.col("total_nilai")
            .rank(method="dense", descending=True)
            .over("kategori")
            .alias("peringkat_dalam_kategori")
        )
        .filter(pl.col("peringkat_dalam_kategori") <= 5)
        .select(["kategori", "produk", "total_nilai", "peringkat_dalam_kategori"])
        .sort(["kategori", "peringkat_dalam_kategori"])
    )

    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    for nama, lf, path in [
        ("per_kategori", lf_gold_kat, GOLD_DIR / "per_kategori.parquet"),
        ("per_segmen", lf_gold_seg, GOLD_DIR / "per_segmen.parquet"),
        ("top_produk", lf_gold_top, GOLD_DIR / "top_produk.parquet"),
    ]:
        df = lf.collect()
        pq.write_table(
            df.to_arrow(),
            str(path),
            compression="zstd",
            write_statistics=True,
        )
        log(f"gold_write_{nama}", {"baris": df.shape[0], "path": str(path)})

    print("\n[Gold: Per Kategori]")
    print(pl.read_parquet(GOLD_DIR / "per_kategori.parquet"))
    print("\n[Gold: Per Segmen]")
    print(pl.read_parquet(GOLD_DIR / "per_segmen.parquet"))


if __name__ == "__main__":
    main()
