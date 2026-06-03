#!/usr/bin/env python3
"""Prevalensi stunting per desa (min 10 balita)."""
import pandas as pd

from analitik.lib.config import GOLD, MIN_BALITA_DESA, SILVER

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    balita = pd.read_parquet(SILVER / "data_balita.parquet")
    balita["desa_id"] = balita["desa_id"].astype(str)
    agg = (
        balita.groupby("desa_id")
        .agg(
            n_balita=("balita_id", "count"),
            n_stunting=("stunting", "sum"),
        )
        .reset_index()
    )
    agg = agg[agg["n_balita"] >= MIN_BALITA_DESA]
    agg["prev_pct"] = (100 * agg["n_stunting"] / agg["n_balita"]).round(2)
    agg["bulan"] = "2026-05"

    desa = pd.read_parquet(SILVER / "desa_sumatera_utara.parquet")
    meta = desa[["desa_id", "nama_desa", "kode_kab", "nama_kab"]]
    out = agg.merge(meta, on="desa_id")
    out.to_parquet(GOLD / "prevalensi_stunting.parquet", index=False)
    print(f"[OK] gold/prevalensi_stunting — {len(out)} desa, mean prev {out['prev_pct'].mean():.1f}%")


if __name__ == "__main__":
    main()
