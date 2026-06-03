#!/usr/bin/env python3
"""Indeks risiko 5 dimensi + prioritas top 50 per kabupaten."""
import pandas as pd

from analitik.lib.config import GOLD, SILVER, TOP_N_PER_KAB
from analitik.lib.indeks import hitung_indeks_total

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    prev = pd.read_parquet(GOLD / "prevalensi_stunting.parquet")
    akses = pd.read_parquet(GOLD / "skor_aksesibilitas.parquet")
    stbm = pd.read_parquet(SILVER / "stbm_dtks.parquet")
    for df in (prev, akses, stbm):
        df["desa_id"] = df["desa_id"].astype(str)

    df = prev.merge(akses, on="desa_id").merge(stbm, on="desa_id", suffixes=("", "_stbm"))
    df = hitung_indeks_total(df)
    df = df.sort_values(["kode_kab", "indeks_total"], ascending=[True, False])
    df["rank_kabupaten"] = df.groupby("kode_kab").cumcount() + 1
    df["status"] = "BARU"

    prior = df[df["rank_kabupaten"] <= TOP_N_PER_KAB].copy()
    df.to_parquet(GOLD / "indeks_risiko.parquet", index=False)
    prior.to_parquet(GOLD / "prioritas_desa_bulanan.parquet", index=False)
    print(f"[OK] indeks_risiko {len(df)} desa; prioritas {len(prior)} baris")


if __name__ == "__main__":
    main()
