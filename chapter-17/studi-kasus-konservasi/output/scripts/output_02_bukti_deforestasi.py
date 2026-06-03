#!/usr/bin/env python3
import geopandas as gpd
from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-2-bukti-deforestasi"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    gdf = gpd.read_parquet(GOLD / "deforestasi_aktif.parquet")
    gdf.to_file(OUT / "deforestasi_latest.geojson", driver="GeoJSON")
    print(f"[OK] {len(gdf)} sel deforestasi")


if __name__ == "__main__":
    main()
