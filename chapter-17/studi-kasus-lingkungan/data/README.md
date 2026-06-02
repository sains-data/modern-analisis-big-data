# Data — Studi Kasus Lingkungan

Organisasi sumber data **karhutla Riau** dan lapisan medallion untuk lakehouse akuntabilitas konsesi.

## Struktur folder

```
data/
├── README.md
├── KATALOG-DATA.md
├── sumber/          # unduhan FIRMS, GFW, KLHK SIGAP, CHIRPS, …
├── bronze/
├── silver/
└── gold/
```

## Alur medallion

| Layer | Contoh entitas |
|---|---|
| **Bronze** | `firms_viirs_raw`, `sentinel2_tile_raw`, `konsesi_sigap_raw` |
| **Silver** | `hotspot_verified`, `konsesi_riau`, `gambut_riau`, `ndvi_nbr` |
| **Gold** | `indeks_risiko_karhutla`, `rekam_hotspot_terverifikasi`, `dampak_kesehatan_kabut`, `emisi_karbon_konsesi` |

## Dokumentasi detail

→ **[KATALOG-DATA.md](KATALOG-DATA.md)** — Tabel 17.6 lengkap.

## Sprint 1 — acceptance criteria

- Semua baris katalog terunduh atau diganti sampel Lampiran.  
- Skema Bronze terbaca Sedona; kolom wajib non-null.  
- Spatial: geometri konsesi dan gambut valid di Silver.  

## Aspek hukum data

Poligon konsesi dari sumber publik (KLHK/KPK) untuk penelitian; jangan publikasikan data non-publik di repo terbuka.
