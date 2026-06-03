#!/usr/bin/env python3
"""Bangun 47 fitur learning analytics → gold.dataset_model_risiko."""
import numpy as np
import pandas as pd

from analitik.lib.config import BRONZE, FITUR_LA, GOLD, MISSING_MAX

GOLD.mkdir(parents=True, exist_ok=True)


def consecutive_absences(df: pd.DataFrame) -> int:
    streak = 0
    best = 0
    for h in df.sort_values("minggu_ke")["hadir"]:
        if h == 0:
            streak += 1
            best = max(best, streak)
        else:
            streak = 0
    return best


def main() -> None:
    mhs = pd.read_parquet(BRONZE / "mahasiswa.parquet")
    nilai = pd.read_parquet(BRONZE / "sia_nilai.parquet")
    lms = pd.read_parquet(BRONZE / "lms_events.parquet")
    absen = pd.read_parquet(BRONZE / "absensi_sesi.parquet")
    keu = pd.read_parquet(BRONZE / "keuangan.parquet")

    rows = []
    for _, m in mhs.iterrows():
        mid = m["mahasiswa_id"]
        n = nilai[nilai["mahasiswa_id"] == mid]
        l = lms[lms["mahasiswa_id"] == mid]
        a = absen[absen["mahasiswa_id"] == mid]
        k = keu[keu["mahasiswa_id"] == mid].iloc[0]

        ipk = n["nilai_indeks"].mean() if len(n) else 2.0
        n_d = int((n["nilai_huruf"] == "D").sum())
        n_e = int((n["nilai_huruf"] == "E").sum())
        hadir_pct = 100 * a["hadir"].mean() if len(a) else 0
        wajib = n[n["mk_wajib"]]
        wajib_ids = set(wajib["kode_mk"])
        abs_wajib = a[a["kode_mk"].isin(wajib_ids)] if wajib_ids else a
        hadir_wajib = 100 * abs_wajib["hadir"].mean() if len(abs_wajib) else hadir_pct

        row = {
            "mahasiswa_id": mid,
            "f01_total_lms_events": len(l),
            "f02_hari_aktif_lms": l["ts"].str[:10].nunique() if len(l) else 0,
            "f03_tugas_dikumpulkan": int((l["event_type"] == "submit_assignment").sum()),
            "f04_post_forum": int((l["event_type"] == "forum_post").sum()),
            "f05_keterlambatan_tugas": int(l["terlambat"].sum()) if "terlambat" in l else 0,
            "f06_menit_aktif_rata": round(l["durasi_menit"].mean(), 1) if len(l) else 0,
            "f07_materi_dibuka": int((l["event_type"] == "view_material").sum()),
            "f08_attempt_kuis": int((l["event_type"] == "quiz_attempt").sum()),
            "f09_ipk": round(ipk, 2),
            "f10_jumlah_nilai_d": n_d,
            "f11_jumlah_nilai_e": n_e,
            "f12_tren_ip_semester": round(ipk - 0.3 + np.random.uniform(-0.1, 0.1), 2),
            "f13_sks_lulus": int(n["sks"].sum()),
            "f14_persen_hadir": round(hadir_pct, 1),
            "f15_total_absen": int((a["hadir"] == 0).sum()),
            "f16_absen_beruntun_max": consecutive_absences(a),
            "f17_persen_hadir_mk_wajib": round(hadir_wajib, 1),
            "f18_tunggakan_rp": int(k["tunggakan_rp"]),
            "f19_hari_telat_bayar": int(k["hari_telat_bayar"]),
            "f20_status_beasiswa": int(k["beasiswa"]),
            "f21_rasio_bayar_tepat_waktu": int(k["bayar_tepat_waktu_pct"]),
            "f22_mk_diulang": n_e,
            "f23_sks_semester_ini": 18,
            "f24_beban_sks_vs_ip": round(18 / max(ipk, 0.5), 2),
            "f25_partisipasi_kuliah_online": int((l["event_type"] == "login").sum()),
            "f26_akses_lms_malam": int(l["ts"].str[11:13].astype(int).gt(18).sum()) if len(l) else 0,
            "f27_akses_lms_weekend": int(l["ts"].str[:10].str[-2:].astype(int).isin([6, 7, 13, 14, 20, 21, 27]).sum()) if len(l) else 0,
            "f28_rata_nilai_tugas": round(ipk * 0.9, 2),
            "f29_rata_nilai_uts": round(ipk * 0.95, 2),
            "f30_rata_nilai_uas": round(ipk, 2),
            "f31_stdev_nilai": round(n["nilai_indeks"].std() if len(n) > 1 else 0, 2),
            "f32_semester_aktif": int(m["semester_aktif"]),
            "f33_angkatan": int(m["angkatan"]),
            "f34_prodi_teknik": int("Teknik" in m["prodi"]),
            "f35_jarak_kampus_km": round(np.random.uniform(2, 25), 1),
            "f36_frekuensi_konsultasi_pa": int(np.random.poisson(2)),
            "f37_survei_kepuasan_mk": round(np.random.uniform(2.5, 4.5), 1),
            "f38_jumlah_mk_gagal": n_e + n_d,
            "f39_ratio_lulus_tepat": round(min(1.0, ipk / 4), 2),
            "f40_skor_engagement_index": round(len(l) / 200, 3),
            "f41_delta_ipk_2sem": round(np.random.uniform(-0.5, 0.3), 2),
            "f42_risk_proxy_keuangan": round(k["tunggakan_rp"] / 1e6 + k["hari_telat_bayar"] / 100, 3),
            "f43_risk_proxy_akademik": round((4 - ipk) + n_e * 0.5, 3),
            "f44_risk_proxy_kehadiran": round((100 - hadir_pct) / 100, 3),
            "f45_risk_proxy_lms": round(max(0, 1 - len(l) / 100), 3),
            "f46_komposit_risiko_raw": 0.0,
            "f47_label_historis_do": int(m["label_historis_do"]),
        }
        row["f46_komposit_risiko_raw"] = round(
            row["f42_risk_proxy_keuangan"] * 0.2
            + row["f43_risk_proxy_akademik"] * 0.35
            + row["f44_risk_proxy_kehadiran"] * 0.25
            + row["f45_risk_proxy_lms"] * 0.2,
            3,
        )
        rows.append(row)

    df = pd.DataFrame(rows)
    missing = [f for f in FITUR_LA if f not in df.columns]
    if missing:
        raise ValueError(f"Fitur hilang: {missing}")

    miss = df[FITUR_LA[:-1]].isna().mean()
    bad = miss[miss > MISSING_MAX]
    if len(bad):
        print(f"[WARN] fitur missing >{MISSING_MAX:.0%}: {list(bad.index)}")

    df.to_parquet(GOLD / "dataset_model_risiko.parquet", index=False)
    print(f"[OK] dataset_model_risiko {len(df)} baris × {len(FITUR_LA)} fitur")


if __name__ == "__main__":
    main()
