#!/usr/bin/env python3
"""
output_03_logistik.py — PDF rencana logistik per shelter (reportlab).
"""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-3-logistik"
OUT.mkdir(parents=True, exist_ok=True)

# Kebutuhan dasar per 100 jiwa (parameter tim)
AIR_L_PER_100 = 50
TENDA_PER_100 = 5
PANGAN_KG_PER_100 = 30


def pdf_shelter(path: Path, row: pd.Series, assigned: pd.DataFrame) -> None:
    c = canvas.Canvas(str(path), pagesize=A4)
    w, h = A4
    y = h - 2 * cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, y, f"Rencana Logistik — {row['nama_shelter']}")
    y -= 1 * cm
    c.setFont("Helvetica", 10)
    lines = [
        f"Tanggal: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"ID Shelter: {row['shelter_id']}",
        f"Kapasitas: {int(row['kapasitas']):,} jiwa",
        f"Estimasi pengungsi dialihkan: {int(row['estimasi_pengungsi']):,} jiwa",
        "",
        "Kelurahan terdampak yang diarahkan:",
    ]
    for _, r in assigned.iterrows():
        lines.append(f"  - {r['nama_kel']}: {int(r['estimasi_terdampak']):,} jiwa ({int(r['jarak_m'])} m)")
    pop = int(row["estimasi_pengungsi"])
    lines.extend(
        [
            "",
            "Kebutuhan logistik (estimasi):",
            f"  - Air bersih: {pop * AIR_L_PER_100 // 100:,} liter",
            f"  - Tenda: {max(1, pop * TENDA_PER_100 // 100)} unit",
            f"  - Pangan kering: {pop * PANGAN_KG_PER_100 // 100:,} kg",
        ]
    )
    for line in lines:
        c.drawString(2 * cm, y, line[:90])
        y -= 0.55 * cm
        if y < 2 * cm:
            c.showPage()
            y = h - 2 * cm
    c.save()


def main() -> None:
    routes_path = GOLD / "rute_evakuasi.parquet"
    if not routes_path.exists():
        print("[SKIP] rute_evakuasi belum ada")
        return

    routes = pd.read_parquet(routes_path)
    if routes.empty:
        return

    shelter_agg = routes.groupby(["shelter_id", "nama_shelter", "kapasitas"], as_index=False).agg(
        estimasi_pengungsi=("estimasi_terdampak", "sum")
    )

    for _, sh in shelter_agg.iterrows():
        assigned = routes[routes["shelter_id"] == sh["shelter_id"]]
        pdf_shelter(OUT / f"logistik_shelter_{sh['shelter_id']}.pdf", sh, assigned)

    # Ringkasan
    ringkas = OUT / "logistik_ringkasan.pdf"
    c = canvas.Canvas(str(ringkas), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Ringkasan Logistik Evakuasi — DAS Musi")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    total = int(shelter_agg["estimasi_pengungsi"].sum())
    c.drawString(2 * cm, y, f"Total estimasi pengungsi: {total:,} jiwa")
    y -= 0.7 * cm
    for _, sh in shelter_agg.iterrows():
        c.drawString(2 * cm, y, f"{sh['nama_shelter']}: {int(sh['estimasi_pengungsi']):,} / kap {int(sh['kapasitas']):,}")
        y -= 0.55 * cm
    c.save()

    print(f"[OK] PDF logistik → {OUT} ({len(shelter_agg)} shelter)")


if __name__ == "__main__":
    main()
