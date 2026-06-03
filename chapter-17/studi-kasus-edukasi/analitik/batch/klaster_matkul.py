#!/usr/bin/env python3
"""K-Means bottleneck mata kuliah."""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from analitik.lib.config import BRONZE, GOLD

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    nilai = pd.read_parquet(BRONZE / "sia_nilai.parquet")
    agg = (
        nilai.groupby("kode_mk")
        .agg(
            nama_mk=("nama_mk", "first"),
            rata_indeks=("nilai_indeks", "mean"),
            pct_gagal=("nilai_huruf", lambda s: (s.isin(["D", "E"]).mean() * 100)),
            n_mhs=("mahasiswa_id", "nunique"),
        )
        .reset_index()
    )
    X = StandardScaler().fit_transform(agg[["rata_indeks", "pct_gagal"]])
    agg["klaster"] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(X)
    agg["bottleneck"] = agg["klaster"] == agg.groupby("klaster")["pct_gagal"].transform("idxmax")
    agg["bottleneck"] = agg["bottleneck"] | (agg["pct_gagal"] >= agg["pct_gagal"].quantile(0.75))
    agg.to_parquet(GOLD / "kinerja_matkul.parquet", index=False)
    n = int(agg["bottleneck"].sum())
    print(f"[OK] kinerja_matkul {len(agg)} MK, {n} bottleneck")


if __name__ == "__main__":
    main()
