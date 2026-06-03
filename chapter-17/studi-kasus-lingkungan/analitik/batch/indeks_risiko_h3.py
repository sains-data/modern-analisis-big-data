#!/usr/bin/env python3
"""Hitung I_risiko per H3 + merge agregat FRP harian."""
import pandas as pd

from analitik.lib.config import GOLD, SILVER
from analitik.lib.indeks_risiko import hitung_indeks, tambah_kelas

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    komp = pd.read_parquet(SILVER / "komponen_risiko_h3.parquet")
    idx = hitung_indeks(komp)
    idx = tambah_kelas(idx)

    frp_path = GOLD / "firms_h3_daily.parquet"
    if frp_path.exists():
        frp = pd.read_parquet(frp_path)
        idx = idx.merge(frp, on="h3_id", how="left")
        idx["n_hotspot_24h"] = idx["n_hotspot"].fillna(0).astype(int)

    idx.to_parquet(GOLD / "indeks_risiko_karhutla.parquet", index=False)
    tinggi = idx[idx["indeks"] >= 0.6]
    print(f"[OK] indeks_risiko {len(idx)} sel H3; Tinggi+: {len(tinggi)}")


if __name__ == "__main__":
    main()
