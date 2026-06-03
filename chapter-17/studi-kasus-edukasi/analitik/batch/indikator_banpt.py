#!/usr/bin/env python3
"""Indikator mutu BAN-PT otomatis."""
import pandas as pd

from analitik.lib.config import BRONZE, GOLD

GOLD.mkdir(parents=True, exist_ok=True)


def main() -> None:
    mhs = pd.read_parquet(BRONZE / "mahasiswa.parquet")
    nilai = pd.read_parquet(BRONZE / "sia_nilai.parquet")
    risiko = pd.read_parquet(GOLD / "profil_risiko_mahasiswa.parquet")

    ipk = nilai.groupby("mahasiswa_id")["nilai_indeks"].mean()
    indikator = {
        "semester": "2026-1",
        "jumlah_mahasiswa_aktif": int(mhs["status_aktif"].sum()),
        "ipk_rata_rata": round(ipk.mean(), 2),
        "pct_risiko_tinggi": round(
            100 * risiko["tingkat_risiko"].isin(["KRITIS", "TINGGI"]).mean(), 1
        ),
        "rasio_dosen_mhs": round(25 / len(mhs), 4),
        "lulusan_tepat_waktu_pct": round(100 * (1 - mhs["label_historis_do"].mean()), 1),
        "jumlah_prodi": int(mhs["prodi"].nunique()),
    }
    pd.DataFrame([indikator]).to_parquet(GOLD / "indikator_banpt.parquet", index=False)
    print(f"[OK] indikator_banpt IPK={indikator['ipk_rata_rata']}")


if __name__ == "__main__":
    main()
