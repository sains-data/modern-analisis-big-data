#!/usr/bin/env python3
"""Sel prioritas patroli: tekanan tinggi + patroli rendah → GPX sederhana."""
from pathlib import Path

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    tekanan = pd.read_parquet(GOLD / "tekanan_kawasan.parquet")
    gap = tekanan[
        (tekanan["indeks_tekanan"] >= tekanan["indeks_tekanan"].quantile(0.75))
        & (tekanan["densitas_patroli"] <= tekanan["densitas_patroli"].median())
    ].head(10)
    gap.to_parquet(GOLD / "coverage_gap.parquet", index=False)

    gpx_dir = OUTPUT_DIR / "output-3-laporan-kel-eudr"
    gpx_dir.mkdir(parents=True, exist_ok=True)
    gpx = gpx_dir / "rute_patroli_prioritas.gpx"
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="FKL Lab">',
        "  <trk><name>Prioritas Patroli</name><trkseg>",
    ]
    for _, r in gap.iterrows():
        lines.append(f'    <trkpt lat="{r.latitude}" lon="{r.longitude}"></trkpt>')
    lines += ["  </trkseg></trk>", "</gpx>"]
    gpx.write_text("\n".join(lines))
    print(f"[OK] coverage_gap {len(gap)} sel + {gpx}")


if __name__ == "__main__":
    main()
