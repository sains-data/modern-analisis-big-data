# Katalog Data — Analitik Stunting Sumatera Utara

Merujuk **Tabel 17.10** (`chapter-17.tex`).

## Katalog sumber

| Dataset | Sumber | Format | Pembaruan | Folder `sumber/` |
|---|---|---|---|---|
| Data gizi balita (e-PPGBM) | Simulasi / API Kemkes | CSV | Bulanan | `eppgbm/` |
| Posyandu / Puskesmas | [Fasyankes](https://fasyankes.kemkes.go.id) | CSV/API | Triwulan | `fasyankes/` |
| Batas desa | BIG / [GADM](https://gadm.org) | GeoPackage | Tahunan | `batas/desa_sumut/` |
| Jaringan jalan | [Geofabrik OSM](https://download.geofabrik.de) | PBF | Mingguan | `osm/indonesia-sumut/` |
| Sanitasi STBM | [stbm.kemkes.go.id](https://stbm.kemkes.go.id) | CSV | Triwulan | `stbm/` |
| Sosial ekonomi | [BPS Sumut](https://sumut.bps.go.id) | XLSX | Tahunan | `bps/sosial/` |
| Kepadatan populasi | [WorldPop](https://www.worldpop.org) | GeoTIFF | Tahunan | `demografi/worldpop/` |
| DEM | NASA SRTM | GeoTIFF | Statis | `dem/srtm/` |

**Tambahan institusional (buku):** DTKS Kemensos (SFTP bulanan) → `sumber/dtks/`.

## Skema medallion

### Bronze

| Tabel | Catatan |
|---|---|
| `bronze.eppgbm` | Raw upload; simpan versi skema |
| `bronze.fasyankes` | Koordinat fasilitas |
| `bronze.batas_admin` | Desa, kec, kab |
| `bronze.stbm`, `bronze.dtks` | Indikator sanitasi & kemiskinan |

### Silver

| Tabel | Transformasi |
|---|---|
| `silver.who_lms_standar` | Lambda-Mu-Sigma per usia & JK |
| `silver.data_balita` | Validasi rentang BB/TB |
| `silver.desa_sumatera_utara` | Centroid desa, kode wilayah |
| `silver.waktu_tempuh_puskesmas` | Hasil OSRM per desa |

### Gold

| Tabel | Deskripsi |
|---|---|
| `gold.prevalensi_stunting` | `prev_pct`, `n_balita`, `n_stunting` per desa/bulan |
| `gold.skor_aksesibilitas_fasyankes` | Menit ke Puskesmas terdekat |
| `gold.indeks_risiko_stunting_multifaktor` | `indeks_total` + 5 skor dimensi |
| `gold.rekam_tumbuh_kembang_balita` | Histori individu (enkripsi) |
| `gold.prioritas_desa_bulanan` | Top 50 per kabupaten |

## Stunting — definisi operasional

**Stunting** = z-score **TB/U** &lt; **−2 SD** (WHO 2006 LMS).

Formula z (buku):

\[
Z = \frac{(TB/M)^L - 1}{L \cdot S} \quad (L \neq 0)
\]

Agregasi desa: `HAVING COUNT(*) >= 10` (stabilitas statistik).

## Konvensi penamaan

```
sumber/eppgbm/eppgbm_YYYYMM.csv
gold/prevalensi_stunting/bulan=YYYY-MM/
```

## Gate Silver

1. Mapping kolom e-PPGBM terdokumentasi (spike Sprint 1).  
2. Tidak ada BB &lt; 1 kg atau &gt; 50 kg masuk Silver tanpa flag.  
3. Semua desa punya `desa_id` valid di GADM/BIG.  

## Pengganti offline

| Produksi | Lab |
|---|---|
| e-PPGBM nasional | CSV 5.000 baris simulasi WHO |
| OSRM produksi | Graph subset 3 kabupaten |
| DTKS | CSV agregat desa contoh |
