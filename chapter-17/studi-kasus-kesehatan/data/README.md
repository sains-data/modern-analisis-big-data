# Data — Studi Kasus Kesehatan

Sumber data **stunting & determinan sosial** Sumatera Utara serta medallion lakehouse.

## Struktur folder

```
data/
├── README.md
├── KATALOG-DATA.md      # Tabel 17.10
├── sumber/
├── bronze/
├── silver/
└── gold/
```

## Alur medallion

| Layer | Contoh |
|---|---|
| **Bronze** | `eppgbm_raw`, `fasyankes_raw`, `stbm_raw`, `dtks_raw`, `osm_sumut` |
| **Silver** | `who_lms_standar`, `data_balita_clean`, `desa_sumatera_utara` |
| **Gold** | `prevalensi_stunting`, `skor_aksesibilitas`, `indeks_risiko_multifaktor` |

## Dokumentasi

→ **[KATALOG-DATA.md](KATALOG-DATA.md)**

## Sprint 1

- Bronze `count() > 0`; kolom kunci non-null.  
- Join LMS WHO pada `usia_bulan` + `jenis_kelamin` berhasil.  

## Etika & privasi

Data balita bersifat sensitif; gunakan simulasi di lab, anonimisasi, dan kebijakan retensi sesuai PERMENKES/PDP.
