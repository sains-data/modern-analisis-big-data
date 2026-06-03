# Studi Kasus Lingkungan — Monitoring Karhutla Riau

**Bab 17 · Studi Kasus 2** | Provinsi Riau | Problem-based learning + Scrum (3 sprint)

## Ringkasan skenario

Tim lembaga riset (mitra **KLHK**) membangun sistem analitik untuk pertanyaan hukum: *apakah titik panas kebakaran gambut jatuh di atas area konsesi perkebunan?* Sistem juga harus menghitung **estimasi emisi karbon per konsesi** dan mengaitkan **dampak kesehatan** (ISPU–ISPA) untuk bukti dan advokasi kebijakan.

## Tiga pertanyaan analitik

| # | Pertanyaan | Teknik inti |
|---|---|---|
| 1 | **Di mana** risiko tertinggi hari ini? | Indeks risiko komposit (gambut, FWI, historis, NDVI, drainase) per sel H3 |
| 2 | **Konsesi mana** dengan hotspot terverifikasi? | `ST_Contains` hotspot × poligon konsesi |
| 3 | **Berapa emisi** dan **dampak kesehatan**? | Burned area × faktor emisi IPCC; korelasi lag ISPU–ISPA |

## Mulai praktikum

**→ [eksperimen/](eksperimen/README.md)** · Eksekusi: **`arsitektur-lab/`**

## Navigasi folder

| Folder | Isi | Dokumen detail |
|---|---|---|
| **[eksperimen](eksperimen/README.md)** | Instruksi praktikum | [INSTRUKSI-EKSPERIMEN.md](eksperimen/INSTRUKSI-EKSPERIMEN.md) |
| [arsitektur-lab](arsitektur-lab/README.md) | Kafka, MinIO — jalankan skrip | [PANDUAN-ARSITEKTUR-LAB.md](arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md) |
| [data](data/README.md) | Katalog Tabel 17.6 + medallion | [KATALOG-DATA.md](data/KATALOG-DATA.md) |
| [analitik](analitik/README.md) | Batch NBR, streaming FIRMS, akuntabilitas | [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) |
| [output](output/README.md) | Empat artefak multi-audiens | [PANDUAN-OUTPUT.md](output/PANDUAN-OUTPUT.md) |

## Product backlog (ringkas)

| Sprint | Fokus | Definisi selesai (contoh) |
|---|---|---|
| **1** | Data & Bronze | Semua dataset Tabel 17.6; formula indeks risiko disetujui |
| **2** | Pipeline + analitik | DAG Airflow harian; query akuntabilitas &lt; 60 dtk; korelasi lag ISPU–ISPA |
| **3** | Output + retro | Dasbor Kepler + filter periode; retrospective |

Detail: [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) dan `chapter-17.tex` §Studi Kasus Lingkungan.

## Lab praktikum

```bash
cd arsitektur-lab && bash start.sh
```

[LAMPPIRAN.md](LAMPIRAN.md)

## Status repositori

| Komponen | Status |
|---|---|
| Dokumentasi | ✅ |
| Skrip + pipeline | ✅ |
| Data FIRMS/SIGAP produksi | Unduh tim |
