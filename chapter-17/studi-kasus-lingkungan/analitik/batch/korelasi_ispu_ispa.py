#!/usr/bin/env python3
"""Korelasi Pearson ISPU vs ISPA lag 0–7 hari per kecamatan."""
import pandas as pd

from analitik.lib.config import GOLD, SILVER

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    df = pd.read_parquet(SILVER / "ispu_ispa.parquet")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    rows = []
    for kec, g in df.groupby("kecamatan"):
        g = g.sort_values("tanggal")
        best_lag, best_r = 0, -1.0
        for lag in range(8):
            a = g["ispu"].iloc[lag:].reset_index(drop=True)
            b = g["kunjungan_ispa"].iloc[: len(a)].reset_index(drop=True)
            if len(a) < 10:
                continue
            r = a.corr(b)
            if pd.notna(r) and r > best_r:
                best_r, best_lag = r, lag
        rows.append(
            {
                "kecamatan": kec,
                "lag_hari_optimal": best_lag,
                "korelasi_pearson": round(best_r, 3),
                "signifikan": best_r >= 0.5,
            }
        )
    out = pd.DataFrame(rows)
    out.to_parquet(GOLD / "korelasi_ispu_ispa.parquet", index=False)
    out.to_parquet(GOLD / "lag_optimal_kecamatan.parquet", index=False)
    n_sig = int(out["signifikan"].sum())
    print(f"[OK] korelasi {len(out)} kecamatan; signifikan (r≥0.5): {n_sig}")


if __name__ == "__main__":
    main()
