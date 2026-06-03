#!/usr/bin/env python3
"""Agregat kecepatan ruas per window 15 menit → gold.lalu_lintas."""
import pandas as pd

from analitik.lib.config import GOLD, SILVER
from analitik.lib.traffic import level_kecepatan, warna_kemacetan

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    mapped = pd.read_parquet(SILVER / "probe_mapped.parquet")
    mapped["ts"] = pd.to_datetime(mapped["ts"], utc=True)
    mapped["window"] = mapped["ts"].dt.floor("15min")

    agg = (
        mapped.groupby(["ruas_id", "window"])
        .agg(
            avg_kecepatan=("speed_kmh", "mean"),
            n_probe=("probe_id", "count"),
            volume_kend=("probe_id", "count"),
        )
        .reset_index()
    )
    agg["avg_kecepatan"] = agg["avg_kecepatan"].round(1)
    agg["level_kemacetan"] = agg["avg_kecepatan"].map(level_kecepatan)
    agg["warna"] = agg["level_kemacetan"].map(warna_kemacetan)

    latest = agg.sort_values("window").groupby("ruas_id").tail(1)
    latest.to_parquet(GOLD / "lalu_lintas.parquet", index=False)
    agg.to_parquet(GOLD / "lalu_lintas_historis.parquet", index=False)
    macet = int((latest["level_kemacetan"] == "MACET").sum())
    print(f"[OK] lalu_lintas — {len(latest)} ruas, {macet} MACET")


if __name__ == "__main__":
    main()
