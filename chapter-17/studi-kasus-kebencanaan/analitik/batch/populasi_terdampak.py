#!/usr/bin/env python3
"""
populasi_terdampak.py — ST_Intersects kelurahan × genangan + estimasi populasi.
Jalankan saat siaga referensi >= ORANYE.
"""
import geopandas as gpd
import pandas as pd

from analitik.lib.config import GOLD, SILVER, STASIUN_REF
from analitik.lib.spatial import estimasi_populasi_terdampak

GOLD.mkdir(parents=True, exist_ok=True)


def siaga_aktif() -> bool:
    latest_path = GOLD / "tma_latest.parquet"
    if latest_path.exists():
        ref = pd.read_parquet(latest_path)
        ref = ref[ref["stasiun_id"] == STASIUN_REF]
        if not ref.empty and ref.iloc[0]["siaga"] in ("ORANYE", "MERAH"):
            return True
    path = GOLD / "tma_siaga_hourly.parquet"
    if not path.exists():
        return True
    df = pd.read_parquet(path)
    ref = df[df["stasiun_id"] == STASIUN_REF]
    if ref.empty:
        return True
    return ref["siaga"].isin(["ORANYE", "MERAH"]).any()


def main() -> None:
    if not siaga_aktif():
        print("[SKIP] Siaga belum ORANYE/MERAH — populasi_terdampak kosong")
        pd.DataFrame().to_parquet(GOLD / "populasi_terdampak.parquet", index=False)
        return

    kel = gpd.read_parquet(SILVER / "kelurahan_sumsel.parquet")
    gen = gpd.read_parquet(SILVER / "genangan_aktif.parquet")
    result = estimasi_populasi_terdampak(kel, gen)

    if result.empty:
        print("[WARN] Tidak ada intersection — periksa geometri genangan")
    else:
        total = int(result["estimasi_terdampak"].sum())
        print(f"[OK] estimasi total terdampak: {total:,} jiwa ({len(result)} baris)")

    result.to_parquet(GOLD / "populasi_terdampak.parquet", index=False)


if __name__ == "__main__":
    main()
