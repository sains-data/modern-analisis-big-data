#!/usr/bin/env python3
"""Output 1 — template WhatsApp alert."""
from pathlib import Path

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-1-alert-konflik"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    path = GOLD / "alert_konflik.parquet"
    if not path.exists():
        print("[SKIP]")
        return
    df = pd.read_parquet(path)
    lines = ["[FKL / BBKSDA — Peringatan Konflik Gajah]\n"]
    for _, r in df.iterrows():
        lines.append(
            f"⚠ {r['nama_individu']} ({r['individu_id']})\n"
            f"   Jarak ke {r['desa_terdekat']}: {int(r['jarak_m'])} m\n"
            f"   {r['rekomendasi']}\n"
        )
    (OUT / "pesan_whatsapp_sample.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] {len(df)} pesan → {OUT}")


if __name__ == "__main__":
    main()
