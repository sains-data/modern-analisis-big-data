#!/usr/bin/env python3
"""Log LMS + stream JSONL."""
import json
import random
from pathlib import Path

import pandas as pd

random.seed(63)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "lms" / "events"
OUT.mkdir(parents=True, exist_ok=True)

EVENTS = ["login", "view_material", "submit_assignment", "forum_post", "quiz_attempt"]


def main() -> None:
    base = pd.read_csv(CASE_ROOT / "data" / "sumber" / "sia" / "mahasiswa_base.csv")
    rows = []
    stream = []
    for _, m in base.iterrows():
        risk = m["label_historis_do"]
        n_events = random.randint(5, 30) if risk else random.randint(40, 200)
        for _ in range(n_events):
            ev = random.choice(EVENTS)
            rows.append(
                {
                    "mahasiswa_id": m["mahasiswa_id"],
                    "event_type": ev,
                    "durasi_menit": random.randint(1, 45),
                    "terlambat": int(ev == "submit_assignment" and risk and random.random() < 0.4),
                    "ts": f"2026-05-{random.randint(1,27):02d}T{random.randint(8,22):02d}:00:00Z",
                }
            )
        stream.append(
            {
                "mahasiswa_id": m["mahasiswa_id"],
                "event_type": "login",
                "durasi_menit": 20,
                "ts": "2026-05-27T08:00:00Z",
                "event": "lms.events",
            }
        )

    pd.DataFrame(rows).to_csv(OUT / "lms_events.csv", index=False)
    with (OUT / "lms_stream.jsonl").open("w") as f:
        for s in stream[:100]:
            f.write(json.dumps(s) + "\n")
    print(f"[OK] lms_events.csv ({len(rows)} events)")


if __name__ == "__main__":
    main()
