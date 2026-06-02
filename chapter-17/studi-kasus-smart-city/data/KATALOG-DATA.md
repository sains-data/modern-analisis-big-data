# Katalog Data — Manajemen Transportasi & Udara Kota Medan

Merujuk **Tabel 17.17** (`chapter-17.tex`).

## Katalog

| Dataset | Sumber | Format | Pembaruan | Folder `sumber/` |
|---|---|---|---|---|
| Jaringan jalan | [Geofabrik OSM](https://download.geofabrik.de) | PBF | Mingguan | `osm/medan/` |
| Rute angkutan umum | Simulasi Trans Metro Deli | GTFS/GeoJSON | Bulanan | `transport/gtfs_tmd/` |
| Kualitas udara | [OpenAQ](https://openaq.org) | JSON/API | Per jam | `udara/openaq/` |
| Probe vehicle GPS | Simulasi pola trafik | CSV/stream | Per detik | `probe/gps/` |
| Meteorologi | [BMKG Open Data](https://dataonline.bmkg.go.id) | CSV/API | Per jam | `cuaca/bmkg/` |
| Kecelakaan | Simulasi Korlantas | CSV | Harian | `kecelakaan/` |
| Zona guna lahan | BIG RTRW Medan | Shapefile | Tahunan | `tata_ruang/rtrw/` |
| Populasi kelurahan | [BPS Medan](https://medankota.bps.go.id) | XLSX | Tahunan | `sosial/populasi/` |

**Institusional (buku):** 120 CCTV persimpangan — metadata detektor di `sumber/cctv/` (edge, bukan video mentah di cloud).

## Skema medallion

### Bronze

| Tabel | Catatan |
|---|---|
| `bronze.jalan_medan` | OSM PBF → GeoParquet |
| `bronze.gtfs_tmd` | Stops, routes, shapes |
| `bronze.sensor_udara` | 15 stasiun OpenAQ |
| `bronze.probe_vehicle` | Stream landing |
| `bronze.kecelakaan` | Titik historis |

### Silver

| Tabel | Transformasi |
|---|---|
| `silver.ruas_jalan` | Segmen + `kapasitas_kend_jam` |
| `silver.probe_mapped` | Map-match ke ruas (ST_DWithin 50 m UTM) |
| `silver.pm25_idw` | Grid 500 m + angin |
| `silver.demand_kelurahan` | Populasi × faktor perjalanan |

### Gold

| Tabel | Deskripsi |
|---|---|
| `gold.lalu_lintas` | `avg_kecepatan`, `level_kemacetan`, window 15 mnt |
| `gold.kualitas_udara` | PM₂.₅ per grid/jam, ISPU |
| `gold.korelasi_pm25` | Pearson per ruas, window 4 jam |
| `gold.gap_tmd_kelurahan` | Coverage % radius 400 m |
| `gold.emisi_kecamatan` | Ton CO₂e/NOₓ/PM₂.₅ per hari |

## Ambang gap TMD (buku)

Kelurahan **underserved**: coverage halte TMD **&lt; 30%** dalam radius **400 m**.

## Konvensi

```
sumber/probe/gps_YYYYMMDD.parquet
gold/lalu_lintas/tanggal=YYYY-MM-DD/jam=HH/
```

## Pengganti offline

| Produksi | Lab |
|---|---|
| 120 CCTV live | Simulator volume kendaraan → probe |
| OpenAQ penuh | 15 stasiun CSV historis 1 bulan |
| GTFS resmi | GTFS sintetis 10 rute TMD |

## Gate Silver

1. Map-match: ≥3 probe per segmen per window.  
2. Grid PM₂.₅: seluruh bbox Kota Medan tanpa null.  
3. GTFS: `stop_id` unik, geometri halte valid.  
