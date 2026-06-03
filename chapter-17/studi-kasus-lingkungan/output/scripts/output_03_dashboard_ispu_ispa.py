#!/usr/bin/env python3
"""Output 3 — ringkasan korelasi ISPU–ISPA untuk dashboard."""
from pathlib import Path

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, SILVER

OUT = OUTPUT_DIR / "output-3-dashboard-ispu-ispa"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    kor = pd.read_parquet(GOLD / "korelasi_ispu_ispa.parquet")
    kor.to_csv(OUT / "korelasi_ringkasan.csv", index=False)

    ispu = pd.read_parquet(SILVER / "ispu_ispa.parquet")
    ispu.tail(500).to_csv(OUT / "ispu_ispa_sample.csv", index=False)

    sig = kor[kor["signifikan"]]
    (OUT / "kecamatan_prioritas.txt").write_text(
        "\n".join(
            f"{r['kecamatan']}: lag {r['lag_hari_optimal']} hari, r={r['korelasi_pearson']}"
            for _, r in sig.iterrows()
        )
        or "(tidak ada korelasi signifikan)",
        encoding="utf-8",
    )
    print(f"[OK] dashboard ISPU–ISPA → {OUT} ({len(sig)} kecamatan signifikan)")


if __name__ == "__main__":
    main()
