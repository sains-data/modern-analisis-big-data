#!/usr/bin/env python3
"""Output 4 — dashboard indikator BAN-PT + ekspor."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-4-banpt"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    ind = pd.read_parquet(GOLD / "indikator_banpt.parquet")
    ind.to_csv(OUT / "indikator_banpt_latest.csv", index=False)

    pdf = OUT / "indikator_banpt_latest.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Indikator Mutu BAN-PT — Ekspor Otomatis (Lab)")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    row = ind.iloc[0]
    for col in ind.columns:
        c.drawString(2 * cm, y, f"{col}: {row[col]}")
        y -= 0.6 * cm
    c.save()
    print(f"[OK] BAN-PT → {pdf}")


if __name__ == "__main__":
    main()
