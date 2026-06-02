# Panduan Arsitektur Lab — Pemantauan KEL

Komponen khas: **edge computing** di hutan (koneksi tidak stabil)—hanya metadata terklasifikasi naik ke cloud.

## Diagram logis

```
┌ INGEST ──────────────────────────────────────────────────────────┐
│ GPS collar→Kafka │ Camera trap→Edge │ Acoustic→Edge │ SMART │ S2 │
└───────┬──────────────────┬─────────────────────────────────────┘
        │                  │
        │ EDGE (stasiun)   │ langsung / batch
        │ YOLOv8-nano      │
        │ CNN chainsaw     │
        └────────┬─────────┘
                 ▼
┌ PEMROSESAN CLOUD (Sedona + Airflow + Spark Streaming) ───────────┐
│ Batch bulanan: NDVI diff, KDE home range, join tekanan, gap    │
│ Stream: alert gajah <2 km; forward deteksi chainsaw            │
└────────────────────────────┬───────────────────────────────────┘
                             ▼
              LAKEHOUSE — pergerakan | deforestasi | tekanan
                            konflik | efektivitas_patroli
                             ▼
        KDE | Gi* | Random Forest | Coverage gap | Least-cost path
                             ▼
     Alert konflik | Bukti deforestasi | Laporan EUDR | DB pergerakan
```

## Edge layer

| Model | Input | Output ke cloud |
|---|---|---|
| YOLOv8-nano | Kamera jebak | Spesies (gajah, harimau, …) — latensi &lt;200 ms |
| CNN 1D audio | Sensor akustik | Deteksi chainsaw (~92% sens.) |

**Penghematan bandwidth:** ~50× vs unggah semua rekaman mentah.

## Topik Kafka

| Topik | Arah |
|---|---|
| `gps.collar.leuser` | In — uplink 4 jam |
| `acoustic.classified.leuser` | In — dari edge |
| `output.alert.konflik` | Out — WhatsApp + dashboard BBKSDA |

**SLO alert gajah:** &lt; **5 menit** (jarak &lt; 2 km ke permukiman).

## DAG Airflow (batch bulanan)

| Task | Fungsi |
|---|---|
| `deteksi_deforestasi` | ΔNDVI bulan berjalan vs sebelumnya |
| `rekonstruksi_home_range` | KDE per individu (50% / 95% contour) |
| `join_tekanan` | Overlay satwa × konsesi × deforestasi |
| `coverage_gap` | Indeks tekanan + area kurang patroli |

## Indeks tekanan (Persamaan 17.2)

\[
I_{\text{tekanan}} = w_1 D + w_2 P + w_3 A + w_4 K - w_5 R
\]

| Simbol | Makna |
|---|---|
| \(D\) | Laju deforestasi (ha/km²) |
| \(P\) | Lonjakan penurunan NDVI |
| \(A\) | Frekuensi chainsaw/tembakan |
| \(K\) | Konflik historis per sel |
| \(R\) | Densitas patroli (jam/km²) |

Grid: **1 km²**. Bobot \(w_1\ldots w_5\) dikalibrasi dari histori SMART.

## Tabel Gold

| Tabel | Isi |
|---|---|
| `gold.pergerakan_satwa` | Trajektori / titik per individu |
| `gold.deforestasi_aktif` | Piksel/sel dengan ΔNDVI &gt; ambang |
| `gold.tekanan_kawasan` | `I_tekanan` per grid |
| `gold.konflik_georeferensi` | Kejadian + Gi* |
| `gold.efektivitas_patroli` | Coverage SMART |

## Port & layanan (rencana)

| Layanan | Port |
|---|---|
| Kafka | 9092 |
| MinIO | 9000/9001 |
| Airflow | 8080 |
| GeoServer / Kepler (opsional) | 8082 / — |

## Checklist Sprint 1

- [ ] Bronze: batas KEL, Hansen, IUCN habitat  
- [ ] Spike interpolasi GPS + flatten SMART JSON  
- [ ] Silver: 7 individu gajah, gap ≤ 4 jam  

## Checklist Sprint 2

- [ ] Simulasi alert &lt; 5 menit, lag &lt; 3 menit  
- [ ] Poligon KDE 50%/95% + % overlap konsesi  
- [ ] Piksel NDVI turun &gt; 0,2 di Gold  

## Etika & tata kelola data

- Lokasi GPS satwa: akses terbatas, jangan publikasikan koordinat presisi di repo terbuka.  
- Kamera jebak: hindari wajah manusia di output demo.

## Rujukan

- [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md)  
- [../analitik/PANDUAN-ANALITIK.md](../analitik/PANDUAN-ANALITIK.md)  
- [../output/PANDUAN-OUTPUT.md](../output/PANDUAN-OUTPUT.md)  
