# Panduan Arsitektur Lab — Transportasi & Udara Kota Medan

Tantangan inti: **memadukan tiga latensi** (ms, detik, 10 menit) dalam satu pipeline.

## Diagram logis

```
┌ INGEST (latensi berbeda) ────────────────────────────────────────┐
│ CCTV/edge(ms) │ GPS TMD/MQTT(s) │ Sensor udara(10m) │ Probe │ SOS │
└────────────────────────────┬───────────────────────────────────┘
                             ▼
              KAFKA (5 topik) + Spark Structured Streaming
              Q1: kecepatan ruas (window 5 mnt) → output.kondisi.jalan /15dtk
              Q2: IDW PM2.5 grid 500m /10 mnt (bobot angin BMKG)
              Q3: join stream korelasi PM2.5 ↔ volume (window 1 jam)
                             │
              BATCH 02:00 WIB (Airflow + Sedona)
              pola historis | estimasi emisi | gap TMD | kecelakaan
                             ▼
              GOLD: lalu_lintas | kualitas_udara | kinerja_tmd
                    kecelakaan | emisi
                             ▼
              Gi* | LSTM | Gap TMD | Gaussian dispersi | DBSCAN
                             ▼
         ATCS Dashboard | IQU warga | Optimasi rute TMD | Laporan emisi
```

## Topik Kafka (Sprint 1)

| Topik | Sumber | Latensi |
|---|---|---|
| `cctv` (atau detektor) | Edge persimpangan | ms |
| `gps.tmd` | Armada Trans Metro Deli | detik |
| `sensor.udara` | 15 stasiun | 10 menit |
| `probe.kendaraan` | Angkot / ride-hailing | detik |
| `media.sosial` | Stream API (opsional) | menit |

**Output internal:** `output.kondisi.jalan` (tiap ~15 detik).

## Ambang kemacetan (Product Owner)

| Level | Kecepatan (km/jam) | Warna ATCS |
|---|---|---|
| LANCAR | ≥ 40 | Hijau |
| PADAT | 20–39 | Kuning |
| MACET | &lt; 20 | Merah |

Minimal **3 probe** per segmen per window (buku).

## Tabel Gold

| Tabel | Granularitas |
|---|---|
| `gold.lalu_lintas` | 15 menit / ruas |
| `gold.kualitas_udara` | Grid 500 m / jam |
| `gold.korelasi_pm25` | Ruas / window 4 jam |
| `gold.kinerja_tmd` | Headway, rute |
| `gold.kecelakaan` | Hotspot |
| `gold.emisi` | Kecamatan / hari |

## Streaming SLO

| Metrik | Target |
|---|---|
| Output kondisi jalan | Setiap **15 detik** |
| Consumer lag | **≤ 10** event |
| Rekomendasi rute alternatif | **&lt; 5 menit** setelah macet (uji Sprint Review) |
| Grid PM₂.₅ | Lengkap tiap **10 menit**, tanpa blank |

## Batch DAG (02:00 WIB)

| Task | Fungsi |
|---|---|
| `pola_historis` | Kecepatan per ruas per jam → LSTM |
| `estimasi_emisi` | CO₂, NOₓ, PM₂.₅ × faktor emisi IPCC |
| `gap_tmd` | Coverage halte vs permintaan |
| `analisis_kecelakaan` | Join kecelakaan × jalan × cuaca |

## IDW PM₂.₅

\(w_i = \frac{1}{d_i^2} \cdot \alpha_i\) — \(\alpha_i\) faktor arah angin (0,5–1,5).

## Port (rencana)

| Layanan | Port |
|---|---|
| Kafka / Kafka UI | 9092 / 8080 |
| Spark UI | 4040 |
| MinIO | 9000/9001 |
| Superset (ATCS/IQU) | 8088 |

## Checklist Sprint 1

- [ ] Bronze: OSM, GTFS, OpenAQ, populasi kelurahan  
- [ ] Producer simulasi 5 topik aktif  
- [ ] Tabel ambang + metrik sukses disetujui  

## Checklist Sprint 2

- [ ] Lag ≤ 10; output 15 detik  
- [ ] Grid 500 m valid  
- [ ] `gold.korelasi_pm25` hari ini  
- [ ] Kelurahan coverage &lt;30% teridentifikasi  

## Rujukan

- [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md)  
- [../analitik/PANDUAN-ANALITIK.md](../analitik/PANDUAN-ANALITIK.md)  
- [../output/PANDUAN-OUTPUT.md](../output/PANDUAN-OUTPUT.md)  
