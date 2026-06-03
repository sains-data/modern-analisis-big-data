#!/usr/bin/env python3
"""Output 2 — CSV + PDF akuntabilitas konsesi."""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-2-akuntabilitas-konsesi"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    path = GOLD / "hotspot_konsesi_agg.parquet"
    if not path.exists() or path.stat().st_size == 0:
        print("[SKIP] tidak ada data akuntabilitas")
        return
    agg = pd.read_parquet(path)
    agg.to_csv(OUT / "akuntabilitas_latest.csv", index=False)

    pdf = OUT / "akuntabilitas_latest.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Laporan Akuntabilitas Konsesi — Karhutla Riau")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    c.drawString(2 * cm, y, f"Tanggal: {datetime.now(timezone.utc).date()}")
    y -= 1 * cm
    for _, r in agg.iterrows():
        line = (
            f"{r['nama_perusahaan']}: {int(r['n_hotspot'])} hotspot | "
            f"FRP {r['total_frp_mw']:.0f} MW | {r['status_kepatuhan']}"
        )
        c.drawString(2 * cm, y, line[:95])
        y -= 0.55 * cm
    c.save()
    print(f"[OK] akuntabilitas → {OUT}")


if __name__ == "__main__":
    main()
