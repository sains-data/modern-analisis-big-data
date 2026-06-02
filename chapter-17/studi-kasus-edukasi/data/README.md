# Data — Studi Kasus Edukasi

Data institusional perguruan tinggi (simulasi/anonim) untuk learning analytics dan akreditasi.

## Struktur

```
data/
├── README.md
├── KATALOG-DATA.md
├── sumber/
├── bronze/
├── silver/
└── gold/
```

## Medallion

| Layer | Contoh |
|---|---|
| **Bronze** | `sia_nilai`, `lms_events`, `absensi`, `lowongan_kerja` |
| **Silver** | `nilai_akademik`, `bimbingan_akademik`, `jadwal_kuliah` |
| **Gold** | `profil_risiko`, `dataset_model_risiko`, `skill_gap` |

## Dokumentasi

→ **[KATALOG-DATA.md](KATALOG-DATA.md)**

## Etika

Jangan commit data mahasiswa asli. Gunakan dataset sintetis Lampiran.
