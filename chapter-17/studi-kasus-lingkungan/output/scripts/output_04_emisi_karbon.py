#!/usr/bin/env python3
"""Output 4 — emisi CO2e per konsesi."""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-4-emisi-karbon"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    path = GOLD / "emisi_karbon_konsesi.parquet"
    if not path.exists():
        print("[SKIP] emisi belum dihitung")
        return
    em = pd.read_parquet(path)
    em.to_csv(OUT / "emisi_per_konsesi_latest.csv", index=False)

    pdf = OUT / "emisi_ringkasan_kejadian.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Estimasi Emisi Karbon — Konsesi Riau (IPCC Tier 1 lab)")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    total = em["emisi_ton_co2e"].sum()
    c.drawString(2 * cm, y, f"Total: {total:,.0f} ton CO2e | {datetime.now(timezone.utc).date()}")
    y -= 1 * cm
    for _, r in em.iterrows():
        c.drawString(
            2 * cm,
            y,
            f"{r['nama_perusahaan']}: {r['emisi_ton_co2e']:,.0f} tCO2e ({r['luas_terbakar_ha']} ha)",
        )
        y -= 0.55 * cm
    c.save()
    print(f"[OK] emisi → {OUT}")


if __name__ == "__main__":
    main()
