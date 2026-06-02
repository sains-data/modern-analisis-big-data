# Data — Studi Kasus Konservasi

Data pemantauan **Kawasan Ekosistem Leuser**: satwa liar, patroli, tutupan hutan, dan ancaman antropogenik.

## Struktur

```
data/
├── README.md
├── KATALOG-DATA.md    # Tabel 17.14
├── sumber/
├── bronze/
├── silver/
└── gold/
```

## Medallion (ringkas)

| Layer | Contoh |
|---|---|
| **Bronze** | `gps_collar_raw`, `smart_patrol_raw`, `sentinel2_raw`, `batas_kel` |
| **Silver** | `gps_interpolated`, `trap_detections`, `ndvi_monthly` |
| **Gold** | `pergerakan`, `deforestasi`, `tekanan`, `konflik`, `efektivitas` |

## Dokumentasi

→ **[KATALOG-DATA.md](KATALOG-DATA.md)**

## Sprint 1

- Dataset statis terbaca Sedona.  
- GPS 7 individu: trajektori kontinu (interpolasi).  

## Sensitivitas

GPS collar dan lokasi konflik bersifat sensitif—gunakan data simulasi di repo publik.
