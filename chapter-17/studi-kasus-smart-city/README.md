# Studi Kasus Smart City — Transportasi & Kualitas Udara Medan

**Bab 17 · Studi Kasus 5** | Kota Medan | PBL + Scrum (3 sprint)

## Ringkasan skenario

Gugus tugas **Bappeda** (Dishub, DLH, BPBD) membutuhkan satu sistem yang menyatukan **120 CCTV**, **15 sensor udara**, dan **GPS armada Trans Metro Deli (TMD)**—saat ini terpisah per dinas, dengan latensi dan protokol berbeda.

## Tiga pertanyaan analitik

| # | Pertanyaan | Teknik inti |
|---|---|---|
| 1 | **Di mana/kapan** kemacetan konsisten? | Probe vehicle + map-matching; Gi* per ruas/jam |
| 2 | **Korelasi** volume kendaraan ↔ PM₂.₅? | Join stream; korelasi Pearson window 4 jam |
| 3 | **Kelurahan mana** kekurangan layanan TMD? | Gap analysis demand vs coverage halte (radius 400 m) |

## Mulai praktikum

**→ [eksperimen/](eksperimen/README.md)** · Eksekusi: **`arsitektur-lab/`**

## Navigasi folder

| Folder | Isi | Dokumen detail |
|---|---|---|
| **[eksperimen](eksperimen/README.md)** | Instruksi praktikum | [INSTRUKSI-EKSPERIMEN.md](eksperimen/INSTRUKSI-EKSPERIMEN.md) |
| [arsitektur-lab](arsitektur-lab/README.md) | Kafka multi-topik, streaming | [PANDUAN-ARSITEKTUR-LAB.md](arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md) |
| [data](data/README.md) | Katalog Tabel 17.17 + medallion | [KATALOG-DATA.md](data/KATALOG-DATA.md) |
| [analitik](analitik/README.md) | Probe speed, IDW PM2.5, gap TMD | [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) |
| [output](output/README.md) | ATCS, IQU, rute TMD, emisi | [PANDUAN-OUTPUT.md](output/PANDUAN-OUTPUT.md) |

## Product backlog (ringkas)

| Sprint | Fokus |
|---|---|
| **1** | Bronze + 5 topik Kafka + ambang lancar/padat/macet & ISPU |
| **2** | Streaming 15 dtk; grid PM₂.₅ 500 m; korelasi Gold; gap TMD |
| **3** | Dashboard ATCS + IQU; ekspor emisi; Sprint Review ke “klien” |

Detail: [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) · `chapter-17.tex` §Studi Kasus Smart City.

## Khasus

- **Streaming-first** (latensi ms → detik → 10 menit).  
- SLO kritis: kondisi jalan **&lt;5 menit**; output probe tiap **15 detik**.

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
| CCTV produksi | Metadata saja (edge) |
