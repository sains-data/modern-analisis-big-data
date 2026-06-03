#!/usr/bin/env python3
"""Output 3 — Rekomendasi optimasi TMD."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-3-optimasi-tmd"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    gap = pd.read_parquet(GOLD / "gap_tmd_kelurahan.parquet")
    under = gap[gap["underserved"]].head(10)
    gap.to_csv(OUT / "gap_kelurahan_latest.csv", index=False)

    pdf = OUT / "rekomendasi_tmd_latest.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Rekomendasi Optimasi Trans Metro Deli — Lab Medan")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    c.drawString(2 * cm, y, f"Kelurahan underserved: {int(gap['underserved'].sum())} / {len(gap)}")
    y -= 1 * cm
    for _, r in under.iterrows():
        c.drawString(
            2 * cm,
            y,
            f"• {r['nama_kelurahan']} ({r['kecamatan']}) — demand {r['demand_trip_hari']}/hari",
        )
        y -= 0.55 * cm
        if y < 3 * cm:
            c.showPage()
            y = 27 * cm
    c.save()
    print(f"[OK] TMD → {pdf}")


if __name__ == "__main__":
    main()
