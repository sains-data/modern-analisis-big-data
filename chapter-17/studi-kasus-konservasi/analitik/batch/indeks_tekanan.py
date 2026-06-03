#!/usr/bin/env python3
"""Indeks tekanan per grid 1 km²."""
import pandas as pd

from analitik.lib.config import BRONZE, GOLD
from analitik.lib.tekanan import hitung_indeks_tekanan

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    ndvi = pd.read_parquet(BRONZE / "ndvi_grid.parquet")
    patrol = pd.read_parquet(BRONZE / "smart_patrol.parquet")
    acoustic = pd.read_parquet(BRONZE / "acoustic_events.parquet")

    grid = ndvi[["grid_id", "latitude", "longitude", "delta_ndvi"]].copy()
    grid["lonjakan_ndvi"] = grid["delta_ndvi"]
    grid["laju_deforestasi"] = (grid["delta_ndvi"] > 0.2).astype(float) * 0.5

    # Agregat acoustic & patrol per grid kasar (bin 0.1°)
    acoustic["lat_bin"] = acoustic["latitude"].round(1)
    acoustic["lon_bin"] = acoustic["longitude"].round(1)
    ac_agg = acoustic.groupby(["lat_bin", "lon_bin"]).size().reset_index(name="frekuensi_acoustic")

    patrol["lat_bin"] = patrol["latitude"].round(1)
    patrol["lon_bin"] = patrol["longitude"].round(1)
    pat_agg = patrol.groupby(["lat_bin", "lon_bin"])["durasi_jam"].sum().reset_index(name="densitas_patroli")

    grid["lat_bin"] = grid["latitude"].round(1)
    grid["lon_bin"] = grid["longitude"].round(1)
    grid = grid.merge(ac_agg, on=["lat_bin", "lon_bin"], how="left")
    grid = grid.merge(pat_agg, on=["lat_bin", "lon_bin"], how="left")
    grid["frekuensi_acoustic"] = grid["frekuensi_acoustic"].fillna(0)
    grid["densitas_patroli"] = grid["densitas_patroli"].fillna(0)
    grid["konflik_historis"] = (grid["frekuensi_acoustic"] > 2).astype(float)

    tekanan = hitung_indeks_tekanan(grid)
    tekanan.to_parquet(GOLD / "tekanan_kawasan.parquet", index=False)
    top = tekanan.nlargest(5, "indeks_tekanan")
    print(f"[OK] tekanan_kawasan — max indeks {top['indeks_tekanan'].max():.3f}")


if __name__ == "__main__":
    main()
