#!/usr/bin/env python3
"""Deteksi edge: chainsaw + camera trap metadata."""
import random
from pathlib import Path

import pandas as pd

random.seed(45)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "edge"
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for i in range(40):
    rows.append(
        {
            "event_id": f"AC{i+1}",
            "jenis": random.choice(["chainsaw", "chainsaw", "gunshot", "elephant"]),
            "confidence": round(random.uniform(0.75, 0.98), 2),
            "latitude": round(97.0 + random.uniform(0, 1), 5),
            "longitude": round(3.5 + random.uniform(0, 1.2), 5),
            "ts": f"2026-05-{random.randint(1,27):02d}T{random.randint(0,23):02d}:00:00Z",
        }
    )
pd.DataFrame(rows).to_csv(OUT / "acoustic_classified.csv", index=False)
print(f"[OK] acoustic_classified.csv")
