from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = CASE_ROOT / "data"
SUMBER = DATA_DIR / "sumber"
BRONZE = DATA_DIR / "bronze"
SILVER = DATA_DIR / "silver"
GOLD = DATA_DIR / "gold"
OUTPUT_DIR = CASE_ROOT / "output"

INSTITUTION_SALT = "lab-pt-teknologi-sumatera"
KAFKA_BOOTSTRAP = "localhost:9098"
KAFKA_TOPIC_LMS = "lms.events"
KAFKA_TOPIC_ABSENSI = "absensi.sesi"

AUC_MIN = 0.75
MISSING_MAX = 0.30
SKILL_GAP_MIN = 10
ABSEN_MINGGU_ALERT = 3

RISIKO_LEVEL = [
    (0.75, "KRITIS"),
    (0.50, "TINGGI"),
    (0.25, "SEDANG"),
    (0.0, "RENDAH"),
]

# 47 fitur learning analytics (buku)
FITUR_LA = [
    "f01_total_lms_events",
    "f02_hari_aktif_lms",
    "f03_tugas_dikumpulkan",
    "f04_post_forum",
    "f05_keterlambatan_tugas",
    "f06_menit_aktif_rata",
    "f07_materi_dibuka",
    "f08_attempt_kuis",
    "f09_ipk",
    "f10_jumlah_nilai_d",
    "f11_jumlah_nilai_e",
    "f12_tren_ip_semester",
    "f13_sks_lulus",
    "f14_persen_hadir",
    "f15_total_absen",
    "f16_absen_beruntun_max",
    "f17_persen_hadir_mk_wajib",
    "f18_tunggakan_rp",
    "f19_hari_telat_bayar",
    "f20_status_beasiswa",
    "f21_rasio_bayar_tepat_waktu",
    "f22_mk_diulang",
    "f23_sks_semester_ini",
    "f24_beban_sks_vs_ip",
    "f25_partisipasi_kuliah_online",
    "f26_akses_lms_malam",
    "f27_akses_lms_weekend",
    "f28_rata_nilai_tugas",
    "f29_rata_nilai_uts",
    "f30_rata_nilai_uas",
    "f31_stdev_nilai",
    "f32_semester_aktif",
    "f33_angkatan",
    "f34_prodi_teknik",
    "f35_jarak_kampus_km",
    "f36_frekuensi_konsultasi_pa",
    "f37_survei_kepuasan_mk",
    "f38_jumlah_mk_gagal",
    "f39_ratio_lulus_tepat",
    "f40_skor_engagement_index",
    "f41_delta_ipk_2sem",
    "f42_risk_proxy_keuangan",
    "f43_risk_proxy_akademik",
    "f44_risk_proxy_kehadiran",
    "f45_risk_proxy_lms",
    "f46_komposit_risiko_raw",
    "f47_label_historis_do",
]
