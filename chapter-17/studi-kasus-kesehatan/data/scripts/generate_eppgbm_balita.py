#!/usr/bin/env python3
"""Data balita sintetis e-PPGBM (~5000 baris) + event upload untuk Kafka."""
import csv
import json
import random
import uuid
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(44)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "eppgbm"
OUT.mkdir(parents=True, exist_ok=True)

DESA_CSV = CASE_ROOT / "data" / "sumber" / "batas" / "desa_sumut.geojson"


def main() -> None:
    import geopandas as gpd

    desa = gpd.read_file(DESA_CSV)
    desa_ids = desa["desa_id"].tolist()
    rows = []
    uploads = []
    base = date(2026, 3, 1)

    for i in range(5000):
        desa_id = random.choice(desa_ids)
        usia = random.randint(0, 60)
        jk = random.choice(["L", "P"])
        # ~22% stunting: TB rendah
        m_ref = 49 + usia * 0.9
        if random.random() < 0.22:
            tb = round(m_ref * random.uniform(0.82, 0.92), 1)
        else:
            tb = round(m_ref * random.uniform(0.94, 1.08), 1)
        bb = round(tb * random.uniform(0.12, 0.18), 2)
        balita_id = f"B{uuid.uuid4().hex[:10]}"
        rows.append(
            {
                "balita_id": balita_id,
                "desa_id": desa_id,
                "usia_bulan": usia,
                "jenis_kelamin": jk,
                "tb_cm": tb,
                "bb_kg": bb,
                "tanggal_ukur": (base + timedelta(days=random.randint(0, 60))).isoformat(),
            }
        )
        if i < 200 and random.random() < 0.15:
            uploads.append(
                {
                    "event": "balita.upload",
                    "balita_id": balita_id,
                    "desa_id": desa_id,
                    "tb_cm": tb,
                    "bb_kg": bb,
                    "bb_kg_prev": round(bb + random.uniform(0.1, 0.5), 2),
                    "usia_bulan": usia,
                    "jenis_kelamin": jk,
                    "bulan_absen": random.choice([0, 0, 0, 2]),
                    "ts": f"2026-05-27T{random.randint(8,16):02d}:00:00Z",
                }
            )

    path = OUT / "eppgbm_202605.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    with (OUT / "upload_events.jsonl").open("w") as f:
        for u in uploads:
            f.write(json.dumps(u) + "\n")
    print(f"[OK] {path} ({len(rows)} balita, {len(uploads)} event upload)")


if __name__ == "__main__":
    main()
