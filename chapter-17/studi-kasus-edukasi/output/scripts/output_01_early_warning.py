#!/usr/bin/env python3
"""Output 1 — notifikasi mingguan dosen PA."""
import json

import pandas as pd

from analitik.lib.config import GOLD, OUTPUT_DIR, SILVER

OUT = OUTPUT_DIR / "output-1-early-warning-pa"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    profil = pd.read_parquet(GOLD / "profil_risiko_mahasiswa.parquet")
    bimbingan = pd.read_parquet(SILVER / "bimbingan_akademik.parquet")
    shap = pd.read_parquet(GOLD / "shap_importance.parquet").head(5)

    flagged = profil[profil["tingkat_risiko"].isin(["KRITIS", "TINGGI"])].merge(
        bimbingan, on="mahasiswa_id", how="left"
    )
    flagged.to_csv(OUT / "notifikasi_pa_latest.csv", index=False)

    ringkasan = (
        flagged.groupby("dosen_pa_id")
        .agg(n_kritis=("tingkat_risiko", lambda s: (s == "KRITIS").sum()), n_tinggi=("tingkat_risiko", lambda s: (s == "TINGGI").sum()))
        .reset_index()
    )
    ringkasan.to_csv(OUT / "ringkasan_pa_per_dosen.csv", index=False)

    top_factors = shap["fitur"].tolist()
    (OUT / "faktor_risiko_top5.json").write_text(
        json.dumps({"faktor_utama_shap": top_factors}, indent=2, ensure_ascii=False)
    )
    print(f"[OK] EWS PA → {OUT} ({len(flagged)} mahasiswa KRITIS/TINGGI)")


if __name__ == "__main__":
    main()
