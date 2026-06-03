# Studi Kasus Edukasi — Big Data Manajemen Akademik PT

**Bab 17 · Studi Kasus 6** | Perguruan tinggi teknik | PBL + Scrum (3 sprint)

## Ringkasan skenario

Rektor membutuhkan jawaban: *mahasiswa mana yang akan berhenti kuliah semester depan?* Data tersebar di **delapan sistem** (SIA, LMS, absensi, keuangan, jadwal, tracer study, dll.). Unit analitik data ditugaskan membangun sistem terpadu untuk prediksi risiko, optimasi operasional, dan dasbor mutu akreditasi.

## Empat pertanyaan analitik

| # | Pertanyaan | Teknik inti |
|---|---|---|
| 1 | **Mahasiswa mana** berisiko DO/gagal? | Learning analytics (47 fitur) + XGBoost + SHAP |
| 2 | **Mata kuliah bottleneck** kelulusan? | K-Means klaster performa lintas angkatan |
| 3 | **Optimasi** jadwal & ruang? | Utilisasi aktual vs kapasitas; ILP/heuristik |
| 4 | **Skill gap** lulusan vs industri? | NLP TF-IDF lowongan × kurikulum CPL |

## Mulai praktikum

**→ [eksperimen/](eksperimen/README.md)** · Eksekusi: **`arsitektur-lab/`**

## Navigasi folder

| Folder | Isi | Dokumen detail |
|---|---|---|
| **[eksperimen](eksperimen/README.md)** | Instruksi praktikum | [INSTRUKSI-EKSPERIMEN.md](eksperimen/INSTRUKSI-EKSPERIMEN.md) |
| [arsitektur-lab](arsitektur-lab/README.md) | Lakehouse, Kafka LMS/absensi | [PANDUAN-ARSITEKTUR-LAB.md](arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md) |
| [data](data/README.md) | Katalog Tabel 17 + medallion | [KATALOG-DATA.md](data/KATALOG-DATA.md) |
| [analitik](analitik/README.md) | Fitur LA, model, NLP | [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) |
| [output](output/README.md) | EWS, jadwal, skill gap, BAN-PT | [PANDUAN-OUTPUT.md](output/PANDUAN-OUTPUT.md) |

## Product backlog (ringkas)

| Sprint | Fokus |
|---|---|
| **1** | Bronze + anonimisasi SHA-256 + katalog 47 fitur |
| **2** | Streaming alert absen; XGBoost AUC ≥0,75; skill gap ≥10 skill |
| **3** | Dashboard PA; ekspor BAN-PT; retrospective privasi |

Detail: [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) · `chapter-17.tex` §Studi Kasus Edukasi.

## Khasus etika

**Privacy by design**: hash NIM, RBAC `profil_risiko`, tidak menampilkan nama di sprint board publik.

## Lab

```bash
cd arsitektur-lab && bash start.sh
```

[LAMPIRAN.md](LAMPIRAN.md)

## Status

| Komponen | Status |
|---|---|
| Dokumentasi | ✅ |
| Skrip + pipeline | ✅ |
| Data SIA produksi | Sintetis / anonim |
