#!/usr/bin/env python3
"""Output 2 — utilisasi ruang & rekomendasi konsolidasi."""
import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-2-utilisasi-ruang"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    util = pd.read_parquet(GOLD / "utilisasi_ruang.parquet")
    rekom_path = GOLD / "rekomendasi_konsolidasi.parquet"
    util.to_csv(OUT / "utilisasi_ruang_latest.csv", index=False)
    if rekom_path.exists():
        pd.read_parquet(rekom_path).to_csv(OUT / "rekomendasi_konsolidasi.csv", index=False)
    tidakk = int((util["status_ruang"] == "TIDAK EFISIEN").sum())
    print(f"[OK] utilisasi ruang → {OUT} ({tidakk} slot TIDAK EFISIEN)")


if __name__ == "__main__":
    main()
