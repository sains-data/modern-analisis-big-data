# Panduan Output — Big Data Perguruan Tinggi

Alur dari **Gold layer** ke empat artefak kebijakan (Gambar `fig:17-output-pt`).

```
Gold (5 tabel Iceberg)
    ├── Output 1 — EWS PA (mingguan)
    ├── Output 2 — Utilisasi ruang (semester)
    ├── Output 3 — Skill gap (tahunan)
    └── Output 4 — Dashboard BAN-PT (otomatis per semester)
```

## Output 1: Early Warning System — Dosen PA

**File:** `output_01_early_warning.py`  
**Jadwal:** Airflow setiap **Senin 07:00**

| Langkah | Detail |
|---|---|
| Sumber | `gold.profil_risiko_mahasiswa` + `silver.bimbingan_akademik` |
| Filter | `tingkat_risiko` ∈ {KRITIS, TINGGI} |
| Agregasi | Ringkasan per `dosen_pa_id`: jumlah kritis/tinggi |
| Simpan | `gold.notifikasi_pa_mingguan/` (partisi `dosen_pa_id`) |
| Visualisasi | Superset: daftar klik-through faktor SHAP |

**Impak:** intervensi sebelum mahasiswa DO; target respons PA &lt; 1 minggu.

Detail: [output-1/README.md](output-1/README.md)

## Output 2: Optimasi penjadwalan & utilisasi ruang

**File:** `output_02_utilisasi_ruang.py`  
**Jadwal:** Akhir semester (sebelum penjadwalan baru)

| Keluaran | Isi |
|---|---|
| Tabel utilisasi | `utilisasi_pct`, `status_ruang` per slot |
| Rekomendasi | Pasangan MK kecil yang bisa dikonsolidasi |
| Simpan | `gold.utilisasi_ruang/` (Iceberg) |

**Impak:** kurangi ruang idle; beban dosen lebih merata.

Detail: [output-2/README.md](output-2/README.md)

## Output 3: Laporan skill gap — revisi kurikulum

**File:** `output_03_laporan_skill_gap.py`  
**Jadwal:** Tahunan (Evaluasi Kurikulum / siklus BAN-PT 4 tahun)

| Kolom laporan | Deskripsi |
|---|---|
| `kata` / skill | Skill industri yang kurang di CPL |
| `frekuensi_pct` | Proporsi di lowongan |
| `matkul_rekomendasi` | MK dengan cosine relevansi tertinggi |

**Impak:** penyisipan topik (mis. cloud, MLOps) ke MK yang sudah ada.

Detail: [output-3/README.md](output-3/README.md)

## Output 4: Dashboard indikator mutu BAN-PT

**File:** `output_04_dashboard_banpt.py`

| Fitur | Detail |
|---|---|
| Sumber | Agregat Gold: lulusan tepat waktu, rasio dosen, IPK, dll. |
| Ekspor | Excel + PDF format borang BAN-PT |
| Visualisasi | Superset real-time/near-real-time terhadap Gold |

**Impak:** mengurangi beban manual tim akreditasi; data konsisten dengan SIA.

Detail: [output-4/README.md](output-4/README.md)

## Kriteria penerimaan Sprint 3

| Output | Definisi selesai |
|---|---|
| 1 | Demo Warek: PA melihat mahasiswa KRITIS + faktor risiko |
| 2 | Rekomendasi konsolidasi tervalidasi BAA |
| 3 | Laporan disetujui Kaprodi; ≥10 skill gap |
| 4 | Ekspor borang berhasil; format sesuai BAN-PT |

## Etika output

- Notifikasi email hanya ke `email_pa` terdaftar.  
- Dashboard PA: filter row-level security per `dosen_pa_id`.  
- Laporan skill gap: agregat, tanpa data individu mahasiswa.

## Rujukan

- [../analitik/PANDUAN-ANALITIK.md](../analitik/PANDUAN-ANALITIK.md)  
- `chapter-17.tex` — §Output Sistem Edukasi
