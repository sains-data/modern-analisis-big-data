#!/usr/bin/env python3
"""
output_04_after_action.py — Laporan after-action (Markdown) untuk BNPB/manajemen.
"""
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, STASIUN_REF

OUT = OUTPUT_DIR / "output-4-after-action"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    hourly = pd.read_parquet(GOLD / "tma_siaga_hourly.parquet")
    ref = hourly[hourly["stasiun_id"] == STASIUN_REF].sort_values("window_end")
    peak = ref.loc[ref["tma_max_cm"].idxmax()] if not ref.empty else None

    pop_path = GOLD / "populasi_terdampak.parquet"
    total_terdampak = 0
    n_kel = 0
    if pop_path.exists():
        pop = pd.read_parquet(pop_path)
        if not pop.empty:
            total_terdampak = int(pop["estimasi_terdampak"].sum())
            n_kel = pop["kode_kel"].nunique()

    routes = GOLD / "rute_evakuasi.parquet"
    n_shelter = 0
    if routes.exists():
        r = pd.read_parquet(routes)
        n_shelter = r["shelter_id"].nunique() if not r.empty else 0

    lines = [
        "# Laporan After-Action — Simulasi Banjir DAS Musi",
        "",
        f"**Dibuat:** {datetime.now(timezone.utc).isoformat()}",
        "",
        "## 1. Ringkasan kejadian",
        "",
    ]
    if peak is not None:
        lines.extend(
            [
                f"- Stasiun referensi **{STASIUN_REF}** mencapai TMA puncak **{peak['tma_max_cm']} cm**",
                f"  pada window `{peak['window_end']}` dengan level **{peak['siaga']}**.",
                f"- Deret observasi: {len(ref)} window 15 menit dalam simulasi lab.",
            ]
        )
    else:
        lines.append("- Data TMA referensi tidak tersedia.")

    lines.extend(
        [
            "",
            "## 2. Kinerja sistem (SLO)",
            "",
            "| Metrik | Target | Catatan lab |",
            "|---|---|---|",
            "| Sensor → peta terdampak | ≤ 5 menit | Pipeline batch/file; ukur di demo Sprint 3 |",
            "| Spatial join | < 60 detik | Python/geopandas pada 50 kelurahan |",
            "| False alarm | Minim | Validasi manual BBWS jika data produksi |",
            "",
            "## 3. Dampak estimasi",
            "",
            f"- **{total_terdampak:,}** jiwa estimasi terdampak di **{n_kel}** kelurahan.",
            f"- **{n_shelter}** shelter digunakan dalam rencana routing.",
            "- Metode: proporsi luas genangan ∩ kelurahan × populasi BPS (asumsi kepadatan merata).",
            "",
            "## 4. Lessons learned (Scrum)",
            "",
            "- Sprint 1: anonimisasi tidak diperlukan; fokus kualitas geometri dan CRS.",
            "- Sprint 2: selaraskan ambang TMA dengan SOP BPBD setempat.",
            "- Sprint 3: uji end-to-end dengan skenario MERAH terdokumentasi.",
            "",
            "## 5. Rekomendasi",
            "",
            "- Tambah sensor hulu DAS; pertimbangkan WorldPop 100 m untuk estimasi populasi.",
            "- Produksi: ganti KNN Euclidean dengan routing jalan + constraint genangan (Sedona).",
            "- Deploy PySpark streaming + Iceberg pada cluster yang sama dengan Bab 16.",
            "",
        ]
    )

    path = OUT / "after_action_latest.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] {path}")


if __name__ == "__main__":
    main()
