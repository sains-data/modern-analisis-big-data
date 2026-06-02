# Panduan Analitik — Big Data Perguruan Tinggi

## Pemetaan sprint

| Sprint | Fokus | Artefak |
|---|---|---|
| 1 | Bronze anonim + katalog 47 fitur | `data/bronze/`, dokumen fitur |
| 2 | Streaming LMS + model risiko + skill gap | `analitik/streaming/`, `analitik/batch/` |
| 2 | Klaster bottleneck MK | `analitik/batch/` atau `notebooks/` |
| 3 | Validasi Kaprodi skill gap; tuning dashboard | [../output/](../output/) |

## 1. Fitur learning analytics (batch)

**File:** `analitik_01_fitur_la.py`

| Dimensi | Fitur (contoh) |
|---|---|
| LMS | f1–f8: total events, hari aktif, tugas, diskusi, pola deadline |
| Akademik | f9–f13: IPK, jumlah nilai D/E, tren semester |
| Absensi | f14–f17: % hadir, total absen |
| Keuangan | tunggakan, status pembayaran (jika tersedia) |

Output: `gold.dataset_model_risiko` — **47 kolom** + label historis DO/gagal.

**Gate:** tidak ada fitur dengan missing &gt;30%.

## 2. Model prediksi risiko (batch)

**File:** `analitik_02_model_risiko.py`

| Langkah | Detail |
|---|---|
| Algoritme | XGBoost / GBTClassifier (Spark MLlib) |
| Split | Train/test stratified (kelas tidak seimbang) |
| Metrik | AUC-ROC ≥ **0,75** |
| Inferensi | Seluruh mahasiswa aktif &lt; **5 menit** |
| Penjelasan | SHAP values per mahasiswa (dashboard PA) |

Output: `gold.profil_risiko_mahasiswa` — `prob_risiko`, `tingkat_risiko` (KRITIS/TINGGI/SEDANG/RENDAH).

## 3. Bottleneck mata kuliah (batch)

**Pertanyaan 2:** MK mana yang menghambat kelulusan?

| Langkah | Metode |
|---|---|
| Agregasi | Nilai rata-rata, % gagal, per angkatan & MK |
| Klasterisasi | K-Means pada vektor performa lintas angkatan |
| Interpretasi | Klaster “bottleneck” → review kurikulum & metode ajar |

Output: `gold.kinerja_matkul`.

## 4. Optimasi jadwal & ruang (batch, akhir semester)

**Pertanyaan 3:** slot/ruang mana tidak efisien?

| Metrik | Definisi |
|---|---|
| `utilisasi_pct` | avg hadir / kapasitas × 100 |
| Status | OPTIMAL (≥80%), CUKUP (≥50%), RENDAH (≥30%), TIDAK EFISIEN |
| Konsolidasi | Pasangan kelas &lt;20 mhs, slot sama, total ≤ kapasitas |

Logika: `output_02_utilisasi_ruang.py` → [../output/output-2/](../output/output-2/).

## 5. Skill gap kurikulum vs industri (batch/NLP)

**File:** `analitik_03_skill_gap.py`

| Langkah | Detail |
|---|---|
| Korpus industri | TF-IDF deskripsi lowongan (LinkedIn/Jobstreet) |
| Korpus kurikulum | TF-IDF CPL / deskripsi MK |
| Gap | Skill/kata frekuensi tinggi di industri, rendah di kurikulum |
| Validasi | ≥ **10** skill gap; disetujui Kaprodi |

Output: `gold.skill_gap_kurikulum`, `gold.rekomendasi_kurikulum` (cosine relevansi MK).

## 6. Streaming — LMS & absensi

| Topik | Pipeline |
|---|---|
| `lms.events` | Agregasi harian → update fitur f1–f8 |
| `absensi.sesi` | Deteksi absen &gt;3 minggu berturut → alert PA |

**SLA (buku):** alert &lt; **60 detik** setelah event; consumer lag &lt; **5**.

File rencana: `analitik/streaming/alert_absensi_pa.py`.

## 7. Indikator BAN-PT (batch)

Agregasi otomatis dari Gold: lulusan tepat waktu, rasio dosen:mahasiswa, IPK rata-rata, dll.

File: `output_04_dashboard_banpt.py` → [../output/output-4/](../output/output-4/).

## Product backlog (ringkas)

| Sprint | User story (inti) | Selesai jika |
|---|---|---|
| 1 | Bronze 4 sumber + hash NIM | Tidak ada NIM asli di Bronze |
| 1 | 47 fitur terdokumentasi | Missing ≤30% per fitur |
| 2 | Streaming alert absen | &lt;60 dtk, lag &lt;5 |
| 2 | XGBoost risiko | AUC ≥0,75; inferensi &lt;5 menit |
| 2 | Skill gap | ≥10 skill; validasi Kaprodi |
| 3 | Dashboard PA klik-through faktor risiko | Demo Warek Akademik |
| 3 | Ekspor BAN-PT Excel/PDF | Format borang sesuai |

## Privasi (analitik)

- Jangan log `nama_mahasiswa` di stdout produksi.  
- SHAP & detail individu hanya via RBAC PA.  
- Notebook eksplorasi: data sintetis saja.

## Rujukan

- [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md)  
- [../arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md](../arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md)  
- `chapter-17.tex` — §Studi Kasus Edukasi
