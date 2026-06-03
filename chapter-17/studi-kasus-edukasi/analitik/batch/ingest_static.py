#!/usr/bin/env python3
import pandas as pd
from analitik.lib.config import BRONZE, SILVER, SUMBER

for p in (BRONZE, SILVER):
    p.mkdir(parents=True, exist_ok=True)


def main() -> None:
    pd.read_csv(SUMBER / "sia" / "mahasiswa_base.csv").to_parquet(BRONZE / "mahasiswa.parquet", index=False)
    pd.read_csv(SUMBER / "sia" / "nilai" / "nilai_semester.csv").to_parquet(BRONZE / "sia_nilai.parquet", index=False)
    pd.read_csv(SUMBER / "lms" / "events" / "lms_events.csv").to_parquet(BRONZE / "lms_events.parquet", index=False)
    pd.read_csv(SUMBER / "absensi" / "absensi_sesi.csv").to_parquet(BRONZE / "absensi_sesi.parquet", index=False)
    pd.read_csv(SUMBER / "keuangan" / "keuangan_mhs.csv").to_parquet(BRONZE / "keuangan.parquet", index=False)
    pd.read_csv(SUMBER / "karir" / "lowongan" / "lowongan_kerja.csv").to_parquet(
        BRONZE / "lowongan_kerja.parquet", index=False
    )
    pd.read_csv(SUMBER / "akademik" / "kurikulum_cpl.csv").to_parquet(BRONZE / "kurikulum.parquet", index=False)
    pd.read_csv(SUMBER / "akademik" / "jadwal" / "jadwal_ruang.csv").to_parquet(
        BRONZE / "jadwal_ruang.parquet", index=False
    )

    mhs = pd.read_parquet(BRONZE / "mahasiswa.parquet")
    bimbingan = mhs[["mahasiswa_id", "dosen_pa_id"]].copy()
    bimbingan.to_parquet(SILVER / "bimbingan_akademik.parquet", index=False)
    print("[OK] ingest")


if __name__ == "__main__":
    main()
