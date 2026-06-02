# Katalog Data — Pemantauan Kawasan Ekosistem Leuser

Merujuk **Tabel 17.14** (`chapter-17.tex`).

## Katalog

| Dataset | Sumber | Format | Pembaruan | Folder `sumber/` |
|---|---|---|---|---|
| Batas KEL | BBKSDA Aceh / KLHK | Shapefile | Tahunan | `batas/kel/` |
| Tutupan hutan | [GFW](https://www.globalforestwatch.org) | GeoTIFF | Tahunan | `tutupan/gfw/` |
| NDVI Sentinel-2 | [Copernicus](https://scihub.copernicus.eu) | GeoTIFF | 5 hari | `satelit/s2_ndvi/` |
| Titik panas MODIS | [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov) | CSV/API | Harian | `firms/modis/` |
| GPS collar satwa | Simulasi pola gajah Leuser | CSV | 4 jam | `satwa/gps_collar/` |
| Patroli SMART | [SMART Tools](https://smartconservationtools.org) | CSV/JSON | Harian | `patroli/smart/` |
| Habitat kritis | [IUCN Red List](https://www.iucnredlist.org) | Shapefile | Tahunan | `habitat/iucn/` |
| Tutupan Hansen | Google Earth Engine / partners | GeoTIFF | Tahunan | `tutupan/hansen/` |

**Tambahan operasional:** peta konsesi perkebunan (institusional), permukiman sekitar KEL → `sumber/sosial/permukiman/`.

## Skema medallion

### Bronze

| Tabel | Catatan |
|---|---|
| `bronze.gps_collar` | JSON/CSV uplink 4 jam |
| `bronze.camera_trap_meta` | Hanya deteksi edge (bukan video mentah) |
| `bronze.acoustic_events` | Flag chainsaw dari edge |
| `bronze.smart_patrol` | JSON hierarkis → perlu flatten |
| `bronze.sentinel2` | Tile NDVI |

### Silver

| Tabel | Transformasi |
|---|---|
| `silver.gps_trajectory` | Interpolasi linear, gap ≤ 4 jam |
| `silver.ndvi_baseline` | Median musiman per piksel |
| `silver.smart_tracks` | Lintasan patroli harian |
| `silver.konsesi_overlap` | Clip ke bbox KEL |

### Gold

| Tabel | Deskripsi |
|---|---|
| `gold.pergerakan_satwa` | Titik + atribut individu |
| `gold.deforestasi_aktif` | ΔNDVI &gt; 0,2 (contoh ambang buku) |
| `gold.tekanan_kawasan` | Grid 1 km², \(I_{\text{tekanan}}\) |
| `gold.konflik_hotspot` | Gi* + historis |
| `gold.home_range_kde` | Poligon 50% / 95% per individu |
| `gold.coverage_gap` | Sel prioritas patroli |

## Ambang analitik (buku)

| Indikator | Ambang |
|---|---|
| Penurunan NDVI deforestasi | &gt; **0,2** bulan berjalan |
| Alert gajah–permukiman | &lt; **2000 m** |
| KDE core home range | Probabilitas ≥ **50%** |
| KDE extent | Probabilitas ≥ **95%** |

## Konvensi

```
sumber/satwa/gps_collar/{individu_id}_YYYYMMDD.csv
gold/tekanan_kawasan/tahun=YYYY/bulan=MM/
```

## Pengganti offline

| Produksi | Lab |
|---|---|
| 7 collar live | CSV simulasi 6 bulan |
| 200 camera trap | Subset deteksi edge |
| SMART penuh | JSON contoh 30 patroli |

## Gate Silver

1. `individu_id` konsisten 7 gajah.  
2. Timestamp UTC + zona WIB terdokumentasi.  
3. SMART flatten: satu baris per segmen patroli.  
