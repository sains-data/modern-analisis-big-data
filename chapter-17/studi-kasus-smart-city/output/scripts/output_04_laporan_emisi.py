#!/usr/bin/env python3
"""Output 4 — Laporan emisi kecamatan."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-4-laporan-emisi"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    emisi = pd.read_parquet(GOLD / "emisi_kecamatan.parquet")
    korel = pd.read_parquet(GOLD / "korelasi_pm25.parquet")
    emisi.to_csv(OUT / "emisi_kecamatan_latest.csv", index=False)

    pdf = OUT / "emisi_kecamatan_latest.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Laporan Emisi Kendaraan — Kota Medan (Lab)")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    c.drawString(2 * cm, y, f"Total CO2: {emisi['co2_kg'].sum():.0f} kg/hari (estimasi lab)")
    y -= 0.8 * cm
    c.drawString(2 * cm, y, f"Korelasi PM2.5–volume max: r={korel['pearson_r'].max():.3f}")
    y -= 1 * cm
    for _, r in emisi.iterrows():
        c.drawString(
            2 * cm,
            y,
            f"{r['kecamatan']}: CO2 {r['co2_kg']:.0f} kg, NOx {r['nox_kg']:.2f} kg, PM2.5 {r['pm25_kg']:.3f} kg",
        )
        y -= 0.55 * cm
    c.save()
    print(f"[OK] emisi → {pdf}")


if __name__ == "__main__":
    main()
