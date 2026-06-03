# Studi Kasus Konservasi — Pemantauan KEL & Konflik Satwa Liar

**Bab 17 · Studi Kasus 4** | Kawasan Ekosistem Leuser (Aceh–Sumut) | PBL + Scrum (3 sprint)

## Ringkasan skenario

**Forum Konservasi Leuser (FKL)** membutuhkan sistem terpadu: GPS collar gajah, kamera jebak, sensor akustik, patroli SMART—saat ini tersebar di laptop individu. Tujuan: tahu **sebelum** konflik gajah–manusia, deteksi deforestasi, dan optimasi rute patroli harian.

## Empat pertanyaan analitik

| # | Pertanyaan | Teknik inti |
|---|---|---|
| 1 | **Di mana** deforestasi aktif bulan ini? | NDVI diff Sentinel-2 multitemporal |
| 2 | **Home range** satwa & overlap konsesi? | KDE GPS collar + `ST_Intersection` |
| 3 | **Di mana** konflik berpotensi? | Gi* kejadian historis × pergerakan GPS |
| 4 | **Area patroli** prioritas hari ini? | Coverage gap SMART + indeks tekanan grid 1 km² |

## Mulai praktikum

**→ [eksperimen/](eksperimen/README.md)** · Eksekusi: **`arsitektur-lab/`**

## Navigasi folder

| Folder | Isi | Dokumen detail |
|---|---|---|
| **[eksperimen](eksperimen/README.md)** | Instruksi praktikum | [INSTRUKSI-EKSPERIMEN.md](eksperimen/INSTRUKSI-EKSPERIMEN.md) |
| [arsitektur-lab](arsitektur-lab/README.md) | Edge + Kafka + MinIO | [PANDUAN-ARSITEKTUR-LAB.md](arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md) |
| [data](data/README.md) | Katalog Tabel 17.14 + medallion | [KATALOG-DATA.md](data/KATALOG-DATA.md) |
| [analitik](analitik/README.md) | KDE, streaming GPS, NDVI batch | [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) |
| [output](output/README.md) | Empat artefak multi-skala waktu | [PANDUAN-OUTPUT.md](output/PANDUAN-OUTPUT.md) |

## Product backlog (ringkas)

| Sprint | Fokus |
|---|---|
| **1** | Bronze statis + GPS Silver (interpolasi) + bobot indeks tekanan |
| **2** | Alert GPS &lt;5 mnt; KDE home range; peta deforestasi Gold |
| **3** | Rute patroli GPX; laporan EUDR PDF/GeoJSON; retrospective |

Detail: [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) · `chapter-17.tex` §Studi Kasus Konservasi.

## Khasus kasus ini

- **Edge computing** di stasiun lapangan (YOLOv8-nano, CNN chainsaw)—hanya data terklasifikasi ke cloud.  
- Data **terbatas** secara etis (GPS collar, tidak semua rekaman kamera mentah).

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
| Data collar produksi | Terbatas / etika |
