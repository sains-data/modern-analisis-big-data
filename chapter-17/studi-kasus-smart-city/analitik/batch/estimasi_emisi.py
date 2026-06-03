#!/usr/bin/env python3
"""Estimasi emisi per kecamatan — volume × faktor emisi IPCC (lab)."""
import geopandas as gpd
import pandas as pd

from analitik.lib.config import EMISI_FAKTOR, GOLD, SILVER

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    mapped = pd.read_parquet(SILVER / "probe_mapped.parquet")
    ruas = gpd.read_parquet(SILVER / "ruas_jalan.parquet")[["ruas_id", "kecamatan"]]
    df = mapped.merge(ruas, on="ruas_id", how="left")

    rows = []
    for (kec, vtype), g in df.groupby(["kecamatan", "vehicle_type"]):
        km = len(g) * 0.5
        ef = EMISI_FAKTOR.get(vtype, EMISI_FAKTOR["mobil"])
        rows.append(
            {
                "kecamatan": kec,
                "vehicle_type": vtype,
                "volume_hari": len(g),
                "km_estimasi": round(km, 1),
                "co2_kg": round(km * ef["co2"] / 1000, 2),
                "nox_kg": round(km * ef["nox"], 3),
                "pm25_kg": round(km * ef["pm25"], 4),
            }
        )
    detail = pd.DataFrame(rows)
    detail.to_parquet(GOLD / "emisi_detail.parquet", index=False)

    agg = (
        detail.groupby("kecamatan")
        .agg(co2_kg=("co2_kg", "sum"), nox_kg=("nox_kg", "sum"), pm25_kg=("pm25_kg", "sum"))
        .reset_index()
    )
    agg.to_parquet(GOLD / "emisi_kecamatan.parquet", index=False)
    print(f"[OK] emisi_kecamatan {len(agg)} kecamatan, total CO2 {agg['co2_kg'].sum():.0f} kg")


if __name__ == "__main__":
    main()
