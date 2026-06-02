# Katalog Data — Peringatan Dini Banjir DAS Musi

Merujuk **Tabel 17.2** (`chapter-17.tex`). Tim mengisi kolom **Lokasi di repo** saat file tersimpan di `data/sumber/` atau Bronze.

## Katalog open source

| Dataset | Sumber | Format | Pembaruan | Pemetaan folder |
|---|---|---|---|---|
| DEM SRTM 30 m | [USGS Earth Explorer](https://earthexplorer.usgs.gov) | GeoTIFF | Statis | `sumber/dem/srtm30/` |
| DEMNAS 8 m | [BIG Tides](https://tides.big.go.id) | GeoTIFF | Statis | `sumber/dem/demnas8/` |
| Batas DAS & sungai | [BIG Tanah Air](https://tanahair.indonesia.go.id) | Shapefile | Tahunan | `sumber/batas/das_musi/` |
| Batas administrasi | BIG / [GADM](https://gadm.org) | GeoPackage | Tahunan | `sumber/batas/admin_sumsel/` |
| Banjir historis | [BNPB Geonode](https://geonode.bnpb.go.id) | Shapefile | Insidental | `sumber/kejadian/banjir_hist/` |
| Curah hujan BMKG | [BMKG Open Data](https://dataonline.bmkg.go.id) | CSV/API | Harian | `sumber/hidrologi/bmkg_hujan/` |
| Citra Sentinel-1 SAR | [Copernicus SciHub](https://scihub.copernicus.eu) | GeoTIFF | ~6 hari | `sumber/satelit/s1_sar/` |
| Sensor TMA | Simulasi historis BBWS | JSON/MQTT | 15 menit | `sumber/sensor/tma_musi/` → Kafka |
| Jalan evakuasi | [Geofabrik OSM](https://download.geofabrik.de) | PBF/GeoJSON | Mingguan | `sumber/jaringan/osm_jalan/` |
| Populasi desa/kelurahan | [BPS Sensus 2020](https://sensus.bps.go.id) | XLSX/CSV | Sensus | `sumber/sosial/bps_populasi/` |

## Skema logis medallion

### Bronze (`data/bronze/`)

| Tabel / prefix | Sumber | Catatan |
|---|---|---|
| `bronze.sensor_tma` | Kafka / JSON file | Kolom: `stasiun_id`, `tma_cm`, `ts` |
| `bronze.bmkg_hujan` | API/CSV harian | Stasiun hulu DAS |
| `bronze.sentinel1_raw` | GeoTIFF tile | Metadata orbit, tanggal akuisisi |
| `bronze.dem`, `bronze.batas_*` | Ingest statis sekali | Partition by `dataset_id` |

### Silver (`data/silver/`)

| Tabel | Validasi |
|---|---|
| `silver.sensor_tma` | Outlier, duplikat timestamp, unit cm |
| `silver.kelurahan` | `ST_IsValid`, SRID 4326, join kode BPS |
| `silver.genangan_sar` | Threshold backscatter / QA mask |
| `silver.jalan` | Topology sederhana, klasifikasi jalan utama |

### Gold (`data/gold/`)

| Tabel | Deskripsi | Pemicu refresh |
|---|---|---|
| `gold.tma_siaga_hourly` | Max/avg TMA + label HIJAU–MERAH per window | Streaming 15 menit |
| `gold.genangan_aktif` | Poligon genangan 1 jam terakhir | Batch SAR / model |
| `gold.populasi_terdampak` | Join kelurahan × genangan, `estimasi_terdampak` | Saat siaga ≥ ORANYE |
| `gold.shelter_kapasitas` | Titik shelter + kapasitas + akses jalan | Batch mingguan |

## Konvensi penamaan file

```
sumber/<kategori>/<dataset_id>_<versi>_<YYYYMMDD>.<ext>
bronze/<tabel>/tahun=YYYY/bulan=MM/...
```

## Kualitas data (Silver gate)

Checklist sebelum promosi Bronze → Silver:

1. **Kelengkapan** — tidak ada stasiun referensi kosong &gt; 2 jam (kecuali maintenance terdokumentasi).  
2. **CRS** — semua geometri EPSG:4326 di Silver; transformasi metrik hanya di query (mis. EPSG:32748).  
3. **Spatial** — `ST_IsValid` = true; bbox dalam [95°E–109°E, 6°S–6°N] untuk subset Sumatera.  
4. **Referensial** — kode kelurahan match BPS; nama kabupaten konsisten GADM.  

## Pengganti offline (praktikum)

| Dataset produksi | Pengganti lab |
|---|---|
| FIRMS / sensor live | Generator JSON TMA 10 stasi (Lampiran) |
| Sentinel-1 lengkap | 1–2 tile GeoTIFF contoh genangan |
| BPS detail | CSV agregat 50 kelurahan sampel Palembang & hulu |

## Referensi metodologis

Estimasi populasi terdampak proporsional luas: lazim dalam studi dampak bencana; keterbatasan asumsi kepadatan merata — alternatif **WorldPop** 100 m (bab mencatat di catatan metodologis).
