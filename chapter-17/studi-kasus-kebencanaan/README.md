# Studi Kasus Kebencanaan — Sistem Peringatan Dini Banjir DAS Musi

**Bab 17 · Studi Kasus 1** | Sumatera Selatan | Problem-based learning + Scrum (3 sprint)

## Ringkasan skenario

Tim ditugaskan **BPBD Provinsi Sumatera Selatan** merancang prototipe sistem peringatan dini banjir yang mengintegrasikan sensor tinggi muka air (TMA), data BMKG, citra satelit, dan peta administrasi—saat ini tersebar di sistem terpisah.

**Deliverable tim (3 sprint):**

1. Pipeline ingest sensor + citra satelit (otomatis)  
2. Estimasi populasi terdampak real-time saat sensor melewati ambang  
3. Dasbor yang dapat dibaca petugas BPBD non-teknis  

## Tiga pertanyaan analitik

| # | Pertanyaan | Teknik inti |
|---|---|---|
| 1 | **Kapan** banjir terjadi? | Prediksi TMA 6–12 jam (LSTM) + curah hujan hulu |
| 2 | **Siapa** terdampak? | Spatial join genangan × kelurahan + populasi BPS |
| 3 | **Ke mana** mengungsi? | KNN join routing evakuasi (jalan tidak tergenang) |

## Mulai praktikum

**→ [eksperimen/](eksperimen/README.md)** — instruksi lengkap: dari folder mana menjalankan kode, urutan langkah, dan apa yang harus dicatat di folder eksperimen.

Titik eksekusi kode: `arsitektur-lab/` (bukan folder `eksperimen/`).

## Navigasi folder

| Folder | Isi | Dokumen detail |
|---|---|---|
| **[eksperimen](eksperimen/README.md)** | **Instruksi & checklist praktikum** | [INSTRUKSI-EKSPERIMEN.md](eksperimen/INSTRUKSI-EKSPERIMEN.md) |
| [arsitektur-lab](arsitektur-lab/README.md) | Stack Docker, Kafka, MinIO — **jalankan skrip di sini** | [PANDUAN-ARSITEKTUR-LAB.md](arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md) |
| [data](data/README.md) | Katalog open data + medallion | [KATALOG-DATA.md](data/KATALOG-DATA.md) |
| [analitik](analitik/README.md) | Streaming, batch Sedona, model | [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md) |
| [output](output/README.md) | Empat artefak ke BPBD/BNPB | [PANDUAN-OUTPUT.md](output/PANDUAN-OUTPUT.md) |

## Product backlog (ringkas)

| Sprint | Fokus | Definisi selesai (contoh) |
|---|---|---|
| **1** | Data & Bronze | Semua dataset Tabel 17.2 di Bronze GeoParquet; skema tervalidasi Sedona |
| **2** | Pipeline + analitik | Streaming TMA → status siaga 15 menit; spatial join populasi &lt; 60 dtk |
| **3** | Output + retro | Dasbor Kepler.gl demo; laporan retrospective |

Detail user story: *Product backlog* tiga sprint di `chapter-17.tex` (lihat [PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md)).

## Lab praktikum

Kode, Docker, dan data sintetis: **[arsitektur-lab/](arsitektur-lab/README.md)** · [LAMPIRAN.md](LAMPIRAN.md)

```bash
cd arsitektur-lab && bash start.sh   # Docker + pipeline penuh
# atau tanpa Docker:
bash scripts/prepare_data.sh && export PYTHONPATH=.. && bash scripts/run_pipeline.sh
```

## Status repositori

| Komponen | Status |
|---|---|
| Dokumentasi Markdown | ✅ |
| Skrip analitik + output 1–4 | ✅ |
| `docker-compose` (Kafka, MinIO) | ✅ |
| Data produksi (BMKG, Sentinel) | Unduh tim — lihat [data/KATALOG-DATA.md](data/KATALOG-DATA.md) |
