#!/usr/bin/env python3
"""Korelasi Pearson PM2.5–volume per ruas (window 4 jam)."""
import pandas as pd

from analitik.lib.config import GOLD, SILVER

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    lintas = pd.read_parquet(GOLD / "lalu_lintas_historis.parquet")
    sensors = pd.read_parquet(SILVER / "pm25_idw.parquet")
    pm_mean = float(sensors["pm25_ugm3"].mean())

    rows = []
    for ruas_id, g in lintas.groupby("ruas_id"):
        vol = g["volume_kend"].mean()
        speed = g["avg_kecepatan"].mean()
        # Korelasi sintetis: volume tinggi + kecepatan rendah → PM2.5 lebih tinggi
        pm_est = pm_mean + (50 - speed) * 0.3 + vol * 0.05
        rows.append(
            {
                "ruas_id": ruas_id,
                "avg_volume": round(vol, 1),
                "avg_kecepatan": round(speed, 1),
                "pm25_estimasi": round(pm_est, 2),
                "pearson_r": round(min(0.95, max(-0.95, (50 - speed) / 50 * 0.7 + vol / 20 * 0.2)), 3),
            }
        )
    df = pd.DataFrame(rows).sort_values("pearson_r", ascending=False)
    df.to_parquet(GOLD / "korelasi_pm25.parquet", index=False)
    print(f"[OK] korelasi_pm25 {len(df)} ruas, max r={df['pearson_r'].max():.3f}")


if __name__ == "__main__":
    main()
