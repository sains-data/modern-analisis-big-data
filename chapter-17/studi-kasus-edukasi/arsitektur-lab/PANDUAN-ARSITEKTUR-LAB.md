# Panduan Arsitektur Lab — Big Data Perguruan Tinggi

Arsitektur **batch mengikuti ritme akademik** + **streaming** untuk LMS dan absensi.

## Diagram logis

```
┌ INGEST (8+ sistem) ──────────────────────────────────────────────┐
│ SIA (harian) │ LMS Moodle→Kafka │ Absensi→Kafka │ Keuangan │ Jobs API │
└────────────────────────────┬───────────────────────────────────┘
                             ▼
        STREAMING                          BATCH (Airflow mingguan)
        • lms.events → fitur harian          • 47 fitur learning analytics
        • absensi.sesi → alert >3 minggu     • Train/inferensi XGBoost
                                               • Utilisasi ruang + jadwal
                                               • NLP skill gap TF-IDF
                             ▼
              GOLD (Iceberg @ MinIO)
              profil_risiko | kinerja_matkul | utilisasi_ruang
              skill_gap | indikator_ban
                             ▼
        XGBoost+SHAP | K-Means MK | Optimasi ruang | NLP | Dashboard mutu
                             ▼
     EWS PA | Rekomendasi jadwal | Laporan skill gap | Dashboard BAN-PT
```

## Topik Kafka

| Topik | Isi |
|---|---|
| `lms.events` | Login, materi, tugas, diskusi |
| `absensi.sesi` | Kehadiran per sesi kuliah |

**Alert:** mahasiswa tidak hadir **&gt;3 minggu** berturut → dosen PA (&lt;60 detik, buku).

## DAG Airflow (ringkas)

| Pipeline | Jadwal | Task utama |
|---|---|---|
| Fitur + model risiko | Mingguan | `analitik_01`, `analitik_02` |
| Utilisasi ruang | Akhir semester | `output_02_utilisasi_ruang` |
| Skill gap NLP | Tahunan / Sprint 3 | `analitik_03_skill_gap` |
| Notifikasi PA | Senin 07:00 | `output_01_early_warning` |
| Indikator BAN-PT | Per semester | `output_04_dashboard_banpt` |

## Tabel Gold

| Tabel | Isi |
|---|---|
| `gold.profil_risiko_mahasiswa` | `prob_risiko`, KRITIS/TINGGI/SEDANG/RENDAH |
| `gold.kinerja_matkul` | Bottleneck per angkatan |
| `gold.utilisasi_ruang` | % utilisasi per slot |
| `gold.skill_gap_kurikulum` | Skill industri vs CPL |
| `gold.indikator_banpt` | Lulusan tepat waktu, rasio dosen:mhs, dll. |

## Privasi (wajib)

| Aturan | Implementasi |
|---|---|
| Anonimisasi | NIM → `mahasiswa_id` = SHA-256(+salt), konsisten lintas sumber |
| Akses | `profil_risiko` hanya dosen PA bimbingan |
| Operasional | Sprint board tanpa nama mahasiswa |

## Model risiko

| Parameter | Nilai buku |
|---|---|
| Algoritme | XGBoost (GBT di Spark MLlib) |
| Fitur | 47 (LMS, nilai, absensi, keuangan) |
| Evaluasi | AUC-ROC ≥ **0,75** (kelas tidak seimbang ~18% risiko) |
| Penjelasan | SHAP per individu |
| Inferensi | Seluruh mahasiswa aktif &lt; **5 menit** |

## Tingkat risiko (inferensi)

| Level | `prob_risiko` |
|---|---|
| KRITIS | ≥ 0,75 |
| TINGGI | ≥ 0,50 |
| SEDANG | ≥ 0,25 |
| RENDAH | &lt; 0,25 |

## Port (rencana)

| Layanan | Port |
|---|---|
| Kafka | 9092 |
| Airflow | 8080 |
| MinIO | 9000/9001 |
| Superset | 8088 |

## Checklist Sprint 1

- [ ] Bronze tanpa NIM asli  
- [ ] 47 fitur terdokumentasi, missing ≤30%  
- [ ] Dokumen pertanyaan + metrik disetujui PO  

## Checklist Sprint 2

- [ ] AUC ≥ 0,75; inferensi &lt; 5 menit  
- [ ] Alert absen &lt; 60 dtk, lag &lt; 5  
- [ ] ≥10 skill gap teridentifikasi  

## Rujukan

- [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md)  
- [../analitik/PANDUAN-ANALITIK.md](../analitik/PANDUAN-ANALITIK.md)  
- [../output/PANDUAN-OUTPUT.md](../output/PANDUAN-OUTPUT.md)  
