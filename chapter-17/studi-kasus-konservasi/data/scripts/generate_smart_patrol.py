#!/usr/bin/env python3
"""Patroli SMART flatten — 30 segmen."""
import json
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(44)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "patroli"
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for i in range(30):
    d = date(2026, 4, 1) + timedelta(days=random.randint(0, 60))
    rows.append(
        {
            "patrol_id": f"PAT{i+1:04d}",
            "ranger": f"Ranger_{random.randint(1,8)}",
            "durasi_jam": round(random.uniform(4, 10), 1),
            "latitude": round(97.0 + random.uniform(0, 1), 5),
            "longitude": round(3.5 + random.uniform(0, 1.2), 5),
            "tanggal": d.isoformat(),
        }
    )
pd.DataFrame(rows).to_csv(OUT / "smart_patrol_flat.csv", index=False)

smart_json = [{"patrol_id": r["patrol_id"], "segments": [r]} for r in rows[:5]]
(OUT / "smart_sample.json").write_text(json.dumps(smart_json, indent=2))
print(f"[OK] smart_patrol_flat.csv ({len(rows)} segmen)")
