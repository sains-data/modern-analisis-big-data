# Katalog Data — Monitoring Karhutla Riau

Merujuk **Tabel 17.6** (`chapter-17.tex`).

## Katalog open source

| Dataset | Sumber | Format | Pembaruan | Folder `sumber/` |
|---|---|---|---|---|
| Titik panas VIIRS | [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov) | CSV/API | 3 jam | `firms/viirs/` |
| Peta gambut | [Global Peatland DB](https://geonode.iwlearn.org) | Shapefile | Tahunan | `gambut/global_peat/` |
| Tutupan lahan | [Global Forest Watch](https://www.globalforestwatch.org) | GeoTIFF | Tahunan | `tutupan/gfw/` |
| Konsesi lahan | [KLHK SIGAP](https://sigap.menlhk.go.id); KPK | Shapefile | Triwulan | `konsesi/sigap/` |
| Citra Sentinel-2 | [Copernicus](https://scihub.copernicus.eu) | GeoTIFF | 5 hari | `satelit/s2/` |
| Indeks FWI | Copernicus CEMS | NetCDF | Harian | `cuaca/fwi/` |
| ISPA puskesmas | Simulasi epidemiologis (lab) | CSV | Harian | `kesehatan/ispa/` |
| Curah hujan | [CHIRPS](https://www.chc.ucsb.edu/data/chirps) | NetCDF | Harian | `hidrologi/chirps/` |

Sumber tambahan di arsitektur buku: **BMKG API**, **SiPongi KLHK** (SFTP historis), **Sentinel Hub** — petakan ke `sumber/` saat tersedia.

## Skema logis medallion

### Bronze

| Tabel / prefix | Catatan |
|---|---|
| `bronze.firms_viirs` | API 3 jam → Kafka atau file landing |
| `bronze.sentinel2` | Tile multi-band per path/row |
| `bronze.konsesi`, `bronze.gambut` | Ingest shapefile/GPKG |
| `bronze.chirps`, `bronze.fwi` | Raster/NetCDF harian |
| `bronze.ispa_sim` | REST simulasi Dinkes |

### Silver

| Tabel | Transformasi |
|---|---|
| `silver.hotspot_firms_verified` | Filter `confidence IN ('nominal','high')`, dedup, CRS 4326 |
| `silver.konsesi_riau` | `nama_perusahaan`, `no_izin`, `jenis_konsesi`, `luas_ha` |
| `silver.gambut_riau` | Clip provinsi Riau |
| `silver.ndvi_nbr` | `RS_MapAlgebra` dari Sentinel-2 |

### Gold

| Tabel | Deskripsi |
|---|---|
| `gold.indeks_risiko_karhutla` | `h3_id`, `tanggal`, `indeks`, komponen \(G,F,H,N,D\) |
| `gold.rekam_hotspot_terverifikasi` | Hotspot + flag dalam konsesi/gambut |
| `gold.hotspot_konsesi_agg` | Agregasi akuntabilitas per perusahaan |
| `gold.dampak_kesehatan_kabut` | `ispu_harian`, `kunjungan_ispa` per kecamatan |
| `gold.korelasi_ispu_ispa` | Korelasi Pearson lag 0–7 |
| `gold.emisi_karbon_konsesi` | Ton CO₂e per konsesi/kejadian |

## Konvensi penamaan

```
sumber/<kategori>/<dataset>_<YYYYMMDD>.<ext>
gold/indeks_risiko_karhutla/tanggal=YYYY-MM-DD/
```

## Gate kualitas Silver

1. **CRS** — simpan EPSG:4326; transformasi metrik hanya di query.  
2. **FIRMS** — koordinat dalam bbox Riau (~99°E–104°E, 0°N–2°N).  
3. **Konsesi** — `ST_IsValid`; overlap gambut tercatat untuk join.  
4. **Citra** — cloud mask &lt; ambang tim (dokumentasikan persen drop).  

## Pengganti offline (praktikum)

| Produksi | Lab |
|---|---|
| FIRMS live | CSV 1 tahun subset Riau (Lampiran) |
| Sentinel-2 penuh | 2 tile + NBR precomputed |
| SIGAP terbaru | 5 poligon konsesi contoh |
| ISPA | Generator CSV pola musiman |

## Referensi hukum (konteks data)

PP 71/2014 jo PP 57/2016 — kewajiban pencegahan kebakaran di konsesi; output akuntabilitas mendukung pembuktian spatial.
