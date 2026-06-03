#!/usr/bin/env python3
"""Output 3 — laporan skill gap kurikulum."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-3-skill-gap"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    gap = pd.read_parquet(GOLD / "skill_gap_kurikulum.parquet")
    gap.to_csv(OUT / "laporan_skill_gap_latest.csv", index=False)

    pdf = OUT / "laporan_skill_gap_latest.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Laporan Skill Gap Kurikulum vs Industri (Lab PT)")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    c.drawString(2 * cm, y, f"Total skill gap teridentifikasi: {len(gap)}")
    y -= 1 * cm
    for _, r in gap.head(15).iterrows():
        c.drawString(
            2 * cm,
            y,
            f"• {r['skill']} — {r['frekuensi_pct']}% lowongan → MK {r['matkul_rekomendasi']}",
        )
        y -= 0.55 * cm
        if y < 3 * cm:
            c.showPage()
            y = 27 * cm
    c.save()
    print(f"[OK] skill gap → {pdf}")


if __name__ == "__main__":
    main()
