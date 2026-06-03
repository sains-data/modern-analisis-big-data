#!/usr/bin/env python3
"""Emisi CO2e per konsesi — burned area × EF (IPCC Tier 1 disederhanakan)."""
import pandas as pd

from analitik.lib.config import EF_GAMBUT_TON_CO2E_PER_HA, GOLD

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    path = GOLD / "hotspot_konsesi_agg.parquet"
    if not path.exists() or path.stat().st_size == 0:
        print("[SKIP] hotspot_konsesi_agg kosong")
        return
    agg = pd.read_parquet(path)
    agg["emisi_ton_co2e"] = (agg["luas_terbakar_ha"] * EF_GAMBUT_TON_CO2E_PER_HA).round(1)
    agg.to_parquet(GOLD / "emisi_karbon_konsesi.parquet", index=False)
    total = agg["emisi_ton_co2e"].sum()
    print(f"[OK] emisi total {total:,.0f} ton CO2e ({len(agg)} konsesi)")


if __name__ == "__main__":
    main()
