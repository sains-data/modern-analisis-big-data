#!/usr/bin/env python3
"""
aggregate_tma.py — Agregasi batch TMA per stasiun (ringkasan terakhir).
Melengkapi streaming window; menulis gold.tma_latest.
"""
import pandas as pd

from analitik.lib.config import GOLD, SILVER, STASIUN_REF
from analitik.lib.siaga import combine_siaga

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    df = pd.read_parquet(SILVER / "sensor_tma.parquet")
    df = df.sort_values("ts")
    latest = df.groupby("stasiun_id", as_index=False).last()

    hujan = pd.read_parquet(SILVER / "bmkg_hujan.parquet")
    hujan_map = hujan.set_index("stasiun_id")["hujan_3jam_mm"].to_dict()

    latest["hujan_3jam_mm"] = latest["stasiun_id"].map(hujan_map).fillna(0)
    latest["siaga"] = latest.apply(
        lambda r: combine_siaga(r["tma_cm"], r["hujan_3jam_mm"]), axis=1
    )
    latest["siaga_order"] = latest["siaga"].map(
        {"HIJAU": 0, "KUNING": 1, "ORANYE": 2, "MERAH": 3}
    )

    ref = latest[latest["stasiun_id"] == STASIUN_REF]
    if not ref.empty:
        print(f"[REF] {STASIUN_REF}: TMA={ref.iloc[0]['tma_cm']} cm → {ref.iloc[0]['siaga']}")

    latest.to_parquet(GOLD / "tma_latest.parquet", index=False)
    print(f"[OK] gold/tma_latest.parquet ({len(latest)} stasiun)")


if __name__ == "__main__":
    main()
