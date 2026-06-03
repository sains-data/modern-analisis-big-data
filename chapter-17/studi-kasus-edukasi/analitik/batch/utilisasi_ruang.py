#!/usr/bin/env python3
"""Utilisasi ruang per slot + rekomendasi konsolidasi."""
import pandas as pd

from analitik.lib.config import BRONZE, GOLD

GOLD.mkdir(parents=True, exist_ok=True)


def status_util(pct: float) -> str:
    if pct >= 80:
        return "OPTIMAL"
    if pct >= 50:
        return "CUKUP"
    if pct >= 30:
        return "RENDAH"
    return "TIDAK EFISIEN"


def main() -> None:
    jadwal = pd.read_parquet(BRONZE / "jadwal_ruang.parquet")
    jadwal["utilisasi_pct"] = (jadwal["hadir_rata"] / jadwal["kapasitas"] * 100).round(1)
    jadwal["status_ruang"] = jadwal["utilisasi_pct"].map(status_util)
    jadwal.to_parquet(GOLD / "utilisasi_ruang.parquet", index=False)

    low = jadwal[jadwal["jumlah_mhs"] < 20].sort_values("jumlah_mhs")
    rekom = []
    for hari in low["hari"].unique():
        subset = low[low["hari"] == hari].head(3)
        if len(subset) >= 2:
            rekom.append(
                {
                    "hari": hari,
                    "mk_konsolidasi": list(subset["kode_mk"]),
                    "total_mhs": int(subset["jumlah_mhs"].sum()),
                    "ruang_usulan": subset.iloc[0]["ruang_id"],
                    "kapasitas": int(subset.iloc[0]["kapasitas"]),
                }
            )
    pd.DataFrame(rekom).to_parquet(GOLD / "rekomendasi_konsolidasi.parquet", index=False)
    tidakk = int((jadwal["status_ruang"] == "TIDAK EFISIEN").sum())
    print(f"[OK] utilisasi_ruang {len(jadwal)} slot, {tidakk} TIDAK EFISIEN")


if __name__ == "__main__":
    main()
