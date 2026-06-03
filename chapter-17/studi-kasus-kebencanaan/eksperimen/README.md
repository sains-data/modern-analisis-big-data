# Eksperimen — Studi Kasus Kebencanaan

**Mulai di sini** jika Anda akan menjalankan kode lab banjir DAS Musi.

Dokumen ini menjawab:
1. **Dari folder mana** eksekusi dimulai  
2. **Urutan perintah** apa yang dijalankan  
3. **Apa yang harus dilakukan** di dalam folder `eksperimen/` (catatan, bukti, checklist)

## Peta singkat

```
studi-kasus-kebencanaan/
├── eksperimen/          ← ANDA DI SINI (baca instruksi, isi catatan)
├── arsitektur-lab/      ← EKSEKUSI KODE dimulai di sini
├── data/                ← hasil generator & medallion (otomatis)
├── analitik/            ← skrip pipeline (dipanggil oleh run_pipeline.sh)
└── output/              ← artefak BPBD (diisi setelah pipeline)
```

## Dokumen dalam folder ini

| File | Untuk apa |
|---|---|
| **[INSTRUKSI-EKSPERIMEN.md](INSTRUKSI-EKSPERIMEN.md)** | Langkah 0–8 lengkap (setup → demo) |
| **[CHECKLIST-SPRINT.md](CHECKLIST-SPRINT.md)** | Centang per sprint Scrum |
| [catatan/template-log-eksperimen.md](catatan/template-log-eksperimen.md) | Salin untuk log harian tim |

## Titik awal eksekusi (wajib)

Semua perintah terminal **dimulai dari**:

```text
sesi-praktikum/chapter-17/studi-kasus-kebencanaan/arsitektur-lab/
```

Bukan dari folder `eksperimen/` dan bukan dari root repositori.

## Jalur cepat (5 menit)

```bash
cd sesi-praktikum/chapter-17/studi-kasus-kebencanaan/arsitektur-lab
chmod +x *.sh scripts/*.sh
bash scripts/prepare_data.sh
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
bash scripts/verify_stack.sh
```

Jika semua `[OK]` → lanjut **Langkah 6–8** di [INSTRUKSI-EKSPERIMEN.md](INSTRUKSI-EKSPERIMEN.md) (verifikasi output & demo).

## Apa yang harus Anda lakukan di folder `eksperimen/`

| Tugas | Lokasi | Kapan |
|---|---|---|
| Baca urutan lab | `INSTRUKSI-EKSPERIMEN.md` | Sebelum terminal |
| Centang sprint | `CHECKLIST-SPRINT.md` | Setelah setiap fase |
| Catat perintah & hasil | `catatan/log-eksperimen-*.md` | Setiap sesi praktikum |
| Screenshot / bukti demo | `catatan/bukti/` (buat sendiri) | Sprint 3 |
| Retrospective tim | `catatan/retrospective-sprint3.md` | Akhir eksperimen |

Folder `eksperimen/` **tidak berisi kode pipeline** — hanya panduan dan dokumentasi hasil kerja Anda.

## Prasyarat

- Python 3.10+  
- Opsional: Docker Desktop (untuk Kafka + MinIO)  
- Sudah mengikuti Bab 9 (Kafka), Bab 11–12 (lakehouse/viz), Bab 16 (geospasial) — konsep, tidak wajib stack yang sama  

## Bantuan

- Error pipeline → lihat bagian *Troubleshooting* di [INSTRUKSI-EKSPERIMEN.md](INSTRUKSI-EKSPERIMEN.md)  
- Detail teknis arsitektur → [../arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md](../arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md)  
- Katalog data produksi → [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md)
