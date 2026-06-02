# Panduan Arsitektur Lab — Monitoring Karhutla Riau

Arsitektur **lima lapisan** (Gambar karhutla Bab 17): Ingest → Pemrosesan (batch + streaming) → Lakehouse Gold → Analitik → Output.

## Diagram logis

```
┌ INGEST ─────────────────────────────────────────────────────────┐
│ FIRMS VIIRS (3 jam) │ BMKG │ Sentinel Hub │ SiPongi │ Dinkes   │
└────────────┬───────────────────────────────┬────────────────────┘
             │ STREAMING                      │ BATCH (02:00 WIB)
             ▼                                ▼
     Kafka + Spark Streaming          Airflow + Sedona
     • H3 res-7 hotspot harian         • NBR / NDVI Sentinel-2
     • ISPA window 7 hari              • ST_Contains join
     • Korelasi lag ISPU–ISPA          • indeks_risiko_karhutla
             │                                │
             └────────────┬───────────────────┘
                          ▼
              LAKEHOUSE (Iceberg @ MinIO)
              indeks_risiko | hotspot_konsesi
              dampak_kesehatan | emisi_karbon
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
           Gi*        XGBoost      Emisi CO₂
         (klaster)   (pred 3 hr)  (burned×EF)
                          ▼
        Peta risiko │ Laporan konsesi │ Dashboard ISPU–ISPA │ NDC
```

## Dua jalur pemrosesan

### Batch (Sedona + Airflow)

| Task DAG (contoh) | Jadwal | Output |
|---|---|---|
| `kalkulasi_nbr` | 02:00 WIB harian | NDVI/NBR Silver |
| `join_spasial` | setelah NBR | hotspot ∩ gambut ∩ konsesi |
| `indeks_risiko` | akhir DAG | `gold.indeks_risiko_karhutla` |

### Streaming (Kafka + Spark)

| Topik Kafka | Window | Output |
|---|---|---|
| `hotspot.firms.riau` | Tumbling harian | Agregat FRP per H3 res-7 |
| `ispa.kecamatan.riau` | Sliding 7 hari | Agregat kunjungan ISPA |

## Tabel Gold (buku)

| Tabel | Granularitas | Pembaruan |
|---|---|---|
| `indeks_risiko` / `indeks_risiko_karhutla` | Sel H3, harian | Batch + refresh streaming |
| `hotspot_konsesi` / `rekam_hotspot_terverifikasi` | Titik + atribut konsesi | Batch join + FIRMS |
| `dampak_kesehatan` | Kecamatan, harian/mingguan | Streaming + batch ISPU |
| `emisi_karbon` | Per konsesi / kejadian | Setelah burned area |

## Formula indeks risiko (Persamaan 17.1)

\[
I_{\text{risiko}} = 0{,}25 G + 0{,}25 F + 0{,}20 H + 0{,}15(1-N) + 0{,}15(1-D)
\]

| Simbol | Komponen |
|---|---|
| \(G\) | Skor kedalaman gambut |
| \(F\) | Fire Weather Index (normalisasi) |
| \(H\) | Densitas historis hotspot 5 tahun |
| \(N\) | NDVI (rendah → risiko tinggi) |
| \(D\) | Jarak ke kanal drainase |

Semua komponen dinormalisasi ke \([0,1]\). Resolusi spasial: **H3 resolusi 7** (~5,16 km/sisi).

## Port layanan (rencana)

| Layanan | Port | Catatan |
|---|---|---|
| Kafka | 9092 | — |
| Airflow UI | 8080 | Bentrok umum dengan YARN — sesuaikan |
| MinIO | 9020/9021 atau 9000 | Pisah dari Ch.16 jika paralel |
| Spark UI | 4040 | — |
| Superset (Output 3) | 8088 | Dashboard publik mingguan |

## Checklist Sprint 1

- [ ] Bronze: FIRMS, gambut, konsesi, CHIRPS/FWI sample  
- [ ] CRS diseragamkan **EPSG:4326** di Silver sebelum join  
- [ ] Dokumen bobot indeks risiko disetujui Product Owner  

## Checklist Sprint 2

- [ ] DAG harian sukses; Gold `indeks_risiko_karhutla` tanggal hari ini  
- [ ] Query akuntabilitas konsesi &lt; 60 dtk (1 tahun hotspot)  
- [ ] `explain()` tanpa CartesianProduct  
- [ ] Tabel korelasi lag 0–7 hari per kecamatan  

## Hambatan umum (Scrum Master)

**CRS mismatch** antara FIRMS (4326) dan shapefile konsesi — wajib `ST_Transform` / validasi di standup Sprint 2 hari pertama.

## Rujukan terkait

- [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md)  
- [../analitik/PANDUAN-ANALITIK.md](../analitik/PANDUAN-ANALITIK.md)  
- [../output/PANDUAN-OUTPUT.md](../output/PANDUAN-OUTPUT.md)  
