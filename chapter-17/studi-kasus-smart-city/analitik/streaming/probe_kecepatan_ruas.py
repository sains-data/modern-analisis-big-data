#!/usr/bin/env python3
"""Simulasi streaming: agregat kecepatan ruas tiap 15 dtk → output.kondisi.jalan."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, SUMBER
from analitik.lib.traffic import level_kecepatan, warna_kemacetan

GOLD.mkdir(parents=True, exist_ok=True)


def load_probe_file() -> pd.DataFrame:
    path = SUMBER / "probe" / "gps" / "probe_stream.jsonl"
    rows = [json.loads(line) for line in path.open()]
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="file")
    _ = parser.parse_args()

    probe = load_probe_file()
    agg = (
        probe.groupby("ruas_id")
        .agg(avg_kecepatan=("speed_kmh", "mean"), n_probe=("probe_id", "count"))
        .reset_index()
    )
    agg["avg_kecepatan"] = agg["avg_kecepatan"].round(1)
    agg["level_kemacetan"] = agg["avg_kecepatan"].map(level_kecepatan)
    agg["warna"] = agg["level_kemacetan"].map(warna_kemacetan)
    agg["ts_emit"] = "2026-05-27T10:00:15Z"

    agg.to_parquet(GOLD / "kondisi_jalan_stream.parquet", index=False)
    out = OUTPUT_DIR / "output-1-atcs"
    out.mkdir(parents=True, exist_ok=True)
    with (out / "kondisi_jalan_stream.jsonl").open("w") as f:
        for _, r in agg.iterrows():
            f.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")
    macet = int((agg["level_kemacetan"] == "MACET").sum())
    print(f"[OK] streaming kondisi jalan — {len(agg)} ruas, {macet} MACET")


if __name__ == "__main__":
    main()
