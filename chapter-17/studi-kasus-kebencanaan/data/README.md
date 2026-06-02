# Data — Studi Kasus Kebencanaan

Folder **data** mengorganisasi sumber data open, hasil unduhan tim, dan struktur **medallion** (Bronze / Silver / Gold) untuk lakehouse banjir DAS Musi.

## Struktur folder

```
data/
├── README.md                 ← halaman ini
├── KATALOG-DATA.md           ← katalog lengkap Tabel 17.2
├── sumber/                   ← salinan mentah dari BMKG, BIG, BPS, OSM, …
├── bronze/                   ← raw feed, raw citra (Iceberg/GeoParquet)
├── silver/                   ← tervalidasi, CRS EPSG:4326
└── gold/                     ← risiko, genangan, populasi_terdampak, siaga TMA
```

Subfolder `sumber/`, `bronze/`, `silver/`, `gold/` siap diisi tim; file besar tidak di-commit (gunakan `.gitignore` di Lampiran).

## Alur medallion (ringkas)

| Layer | Contoh entitas | Transformasi utama |
|---|---|---|
| **Bronze** | `sensor_tma_raw`, `sentinel1_tile_raw` | Ingest apa adanya + metadata ingest |
| **Silver** | `kelurahan_sumsel`, `genangan_valid`, `sensor_tma_clean` | Validasi geometri, CRS, deduplikasi |
| **Gold** | `tma_siaga_hourly`, `populasi_terdampak`, `rute_evakuasi` | Agregasi bisnis, siaga, join spasial |

## Dokumentasi detail

→ **[KATALOG-DATA.md](KATALOG-DATA.md)** — URL, format, frekuensi pembaruan, pemilik sprint 1.

## Sprint 1 — acceptance criteria (data engineer)

- Semua baris Tabel 17.2 terunduh atau tercatat alasan pengganti (simulasi).  
- Skema Bronze terdokumentasi; file dapat dibaca `sedona.read.format("geoparquet")`.  
- Validasi: tidak ada geometri invalid di Silver; sensor TMA lag ingest &lt; 30 detik (uji lab).  

## Catatan

Data sensor TMA pada buku dapat **disimulasikan** dari historis BBWS jika perangkat fisik tidak tersedia. Citra Sentinel-1 membutuhkan akun Copernicus; untuk offline gunakan subset GeoTIFF contoh di Lampiran.
