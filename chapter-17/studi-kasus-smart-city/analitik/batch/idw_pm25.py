#!/usr/bin/env python3
"""IDW PM2.5 grid 500 m + kategori ISPU."""
import pandas as pd

from analitik.lib.config import BRONZE, GOLD, GRID_PM25_M, MEDAN_CENTER, SILVER, SUMBER
from analitik.lib.spatial import idw_pm25
from analitik.lib.traffic import ispu_kategori

GOLD.mkdir(parents=True, exist_ok=True)


def build_grid() -> pd.DataFrame:
    clat, clon = MEDAN_CENTER
    step = GRID_PM25_M / 111_000
    rows = []
    for i in range(-8, 9):
        for j in range(-10, 11):
            rows.append({"grid_id": f"G{i}_{j}", "latitude": clat + i * step, "longitude": clon + j * step})
    return pd.DataFrame(rows)


def main() -> None:
    sensors = pd.read_csv(SUMBER / "udara" / "openaq" / "sensor_latest.csv")
    angin = pd.read_parquet(BRONZE / "bmkg_angin.parquet")
    wind = float(angin.loc[angin["jam"] == 10, "wind_from_deg"].iloc[0])

    grid = build_grid()
    pm = idw_pm25(sensors, grid, wind_from_deg=wind)
    pm[["kategori_ispu", "warna_ispu"]] = pm["pm25_ugm3"].apply(
        lambda v: pd.Series(ispu_kategori(v))
    )
    pm.to_parquet(SILVER / "pm25_idw.parquet", index=False)
    pm.to_parquet(GOLD / "kualitas_udara.parquet", index=False)
    tidak_sehat = int((pm["pm25_ugm3"] > 55.4).sum())
    print(f"[OK] kualitas_udara {len(pm)} sel grid, {tidak_sehat} sel ISPU buruk")


if __name__ == "__main__":
    main()
