"""Audit lintas lapisan Medallion (Bronze / Silver / Gold)."""
from pathlib import Path

import duckdb
import pyarrow.dataset as ds

from paths import BRONZE_TRX, DATALAKE, GOLD_DIR, SILVER_TRX


def ukuran_dir(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(f.stat().st_size for f in path.rglob("*.parquet"))


def main() -> None:
    print("=" * 55)
    print("LAPORAN AUDIT PIPELINE MEDALLION ARROW")
    print("=" * 55)

    ds_bronze = ds.dataset(str(BRONZE_TRX), format="parquet")
    n_bronze = ds_bronze.count_rows()
    print("\n[Bronze]")
    print(f"  Baris      : {n_bronze:,}")
    print(f"  Schema     : {ds_bronze.schema}")

    ds_silver = ds.dataset(
        str(SILVER_TRX),
        format="parquet",
        partitioning="hive",
    )
    n_silver = ds_silver.count_rows()
    print("\n[Silver]")
    print(f"  Baris      : {n_silver:,}")
    print(f"  Partisi    : {ds_silver.partitioning}")
    print(f"  Rejection  : {(n_bronze - n_silver) / max(n_bronze, 1) * 100:.1f}%")

    con = duckdb.connect()
    print("\n[Gold: Validasi Konsistensi]")
    omzet_silver = con.execute(
        f"""
        SELECT ROUND(SUM(total_nilai), 2) AS total
        FROM read_parquet('{SILVER_TRX}/**/*.parquet', hive_partitioning=true)
        """
    ).fetchone()[0]

    omzet_gold = con.execute(
        f"""
        SELECT ROUND(SUM(omzet_total), 2) AS total
        FROM read_parquet('{GOLD_DIR / "per_kategori.parquet"}')
        """
    ).fetchone()[0]

    status = "OK" if omzet_silver == omzet_gold else "MISMATCH"
    print(f"  Omzet Silver : {omzet_silver:,.2f}")
    print(f"  Omzet Gold   : {omzet_gold:,.2f}")
    print(f"  Status       : {status}")

    print("\n[Ukuran Penyimpanan]")
    print(f"  Bronze : {ukuran_dir(DATALAKE / 'bronze'):>12,} byte")
    print(f"  Silver : {ukuran_dir(DATALAKE / 'silver'):>12,} byte")
    gold_names = ["per_kategori", "per_segmen", "top_produk"]
    gold_size = sum(
        (GOLD_DIR / f"{n}.parquet").stat().st_size
        for n in gold_names
        if (GOLD_DIR / f"{n}.parquet").exists()
    )
    print(f"  Gold   : {gold_size:>12,} byte")


if __name__ == "__main__":
    main()
