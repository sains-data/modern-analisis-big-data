#!/usr/bin/env python3
"""Output 4 — PDF skor kebutuhan tenaga kesehatan per desa."""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from analitik.lib.config import GOLD, OUTPUT_DIR, SILVER

OUT = OUTPUT_DIR / "output-4-bukti-nakes"
OUT.mkdir(parents=True, exist_ok=True)


def skor_nakes(row: pd.Series) -> float:
    return (
        0.35 * min(row["prev_pct"] / 40, 1)
        + 0.30 * min(row["waktu_tempuh_menit"] / 120, 1)
        + 0.20 * (1 if row["jumlah_bidan"] == 0 else 0.3)
        + 0.15 * (1 / max(row["kader_aktif"], 1))
    )


def main() -> None:
    prev = pd.read_parquet(GOLD / "prevalensi_stunting.parquet")
    akses = pd.read_parquet(GOLD / "skor_aksesibilitas.parquet")
    stbm = pd.read_parquet(SILVER / "stbm_dtks.parquet")
    df = prev.merge(akses, on="desa_id").merge(stbm, on="desa_id")
    df["skor_kebutuhan_nakes"] = df.apply(skor_nakes, axis=1).round(3)
    df = df.sort_values("skor_kebutuhan_nakes", ascending=False)
    df.head(30).to_csv(OUT / "prioritas_penempatan_nakes.csv", index=False)

    pdf = OUT / "laporan_nakes_ringkasan.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, 27 * cm, "Bukti Pengusulan Tenaga Kesehatan — Sumatera Utara")
    c.setFont("Helvetica", 10)
    y = 26 * cm
    c.drawString(2 * cm, y, f"Tanggal: {datetime.now(timezone.utc).date()}")
    y -= 1 * cm
    c.drawString(2 * cm, y, f"Desa prioritas penempatan (top 15):")
    y -= 0.7 * cm
    for _, r in df.head(15).iterrows():
        line = (
            f"{r['nama_desa']} ({r['nama_kab']}): skor {r['skor_kebutuhan_nakes']:.2f} "
            f"| prev {r['prev_pct']}% | {r['waktu_tempuh_menit']} mnt ke Puskesmas"
        )
        c.drawString(2 * cm, y, line[:95])
        y -= 0.55 * cm
    c.save()
    print(f"[OK] {pdf}")


if __name__ == "__main__":
    main()
