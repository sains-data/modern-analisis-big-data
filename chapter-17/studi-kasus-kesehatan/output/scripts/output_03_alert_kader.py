#!/usr/bin/env python3
"""Output 3 — ringkasan alert untuk kader (dari gold.alert_kader)."""
import json
from pathlib import Path

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR

OUT = OUTPUT_DIR / "output-3-alert-kader"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    path = GOLD / "alert_kader.parquet"
    if not path.exists():
        print("[SKIP] alert_kader belum ada — jalankan alert_kader_stream.py")
        return
    alerts = pd.read_parquet(path)
    summary = alerts.groupby("level").size().reset_index(name="jumlah")
    summary.to_csv(OUT / "ringkasan_alert.csv", index=False)

    with (OUT / "notifikasi_kader_sample.txt").open("w") as f:
        for _, r in alerts.head(10).iterrows():
            f.write(
                f"[{r['level']}] Balita {r['balita_id']} — Desa {r['desa_id']}\n"
                f"  z TB/U: {r['z_tb_u']} | {r['tindak_lanjut']}\n\n"
            )
    print(f"[OK] {len(alerts)} alert — {OUT}")


if __name__ == "__main__":
    main()
