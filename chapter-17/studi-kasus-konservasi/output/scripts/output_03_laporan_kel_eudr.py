#!/usr/bin/env python3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-3-laporan-kel-eudr"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    tekanan = pd.read_parquet(GOLD / "tekanan_kawasan.parquet")
    defor = pd.read_parquet(GOLD / "deforestasi_aktif.parquet")
    gap = pd.read_parquet(GOLD / "coverage_gap.parquet")

    summary = {
        "bulan": "2026-05",
        "n_sel_deforestasi": len(defor),
        "luas_deforestasi_ha": len(defor) * 100,
        "n_sel_tekanan_tinggi": int((tekanan["indeks_tekanan"] >= 0.6).sum()),
        "n_prioritas_patroli": len(gap),
    }
    pd.DataFrame([summary]).to_csv(OUT / "ringkasan_eudr.csv", index=False)

    pdf = OUT / "laporan_kel_latest.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Laporan Monitoring KEL — Format EUDR/GFW (Lab)")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    for k, v in summary.items():
        c.drawString(2 * cm, y, f"{k}: {v}")
        y -= 0.6 * cm
    c.save()
    print(f"[OK] {pdf}")


if __name__ == "__main__":
    main()
