# Panduan Arsitektur Lab — Peringatan Dini Banjir DAS Musi

Dokumen ini merinci arsitektur dari **Gambar arsitektur pipeline** Bab 17 (Studi Kasus Kebencanaan) untuk dipetakan ke komponen di `arsitektur-lab/` saat Lampiran tersedia.

## Pola arsitektur: Lambda (disederhanakan)

```
┌─────────────────────────────────────────────────────────────────┐
│  SUMBER DATA                                                    │
│  Sensor TMA/ARR (MQTT→Kafka) │ Sentinel-1 │ BIG statis │ BPS+OSM │
└──────────────┬──────────────────────────────┬───────────────────┘
               │ STREAMING                    │ BATCH (Airflow+Sedona)
               ▼                              ▼
        Spark Structured Streaming      Job harian / 6 hari
        window 1 jam, slide 15 menit
               │                              │
               └──────────────┬───────────────┘
                              ▼
                    LAKEHOUSE (Iceberg @ MinIO)
                    Bronze → Silver → Gold
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
            LSTM TMA    ST_Intersects   KNN routing
            prediksi    populasi        evakuasi
               │              │              │
               └──────────────┴──────────────┘
                              ▼
              Dasbor │ Notifikasi │ Logistik PDF │ WMS
```

## Lapisan dan teknologi

| Lapisan | Komponen | Peran pada kasus banjir |
|---|---|---|
| Ingest streaming | MQTT → **Kafka** → Spark Structured Streaming | Sensor TMA tiap 15 menit, watermark 30 menit |
| Ingest batch | **Airflow** + **Apache Sedona** | Citra SAR, DEM, batas DAS/admin, OSM |
| Penyimpanan | **MinIO** + **Apache Iceberg** | Tabel medallion, time travel audit |
| Analitik stream | Spark SQL + Sedona | Agregasi window, flag siaga HIJAU–MERAH |
| Analitik batch/model | Sedona SQL, **LSTM** (TMA) | Prediksi 6–12 jam; genangan dari SAR |
| Serving geo | **GeoServer** WMS/WFS (opsional) | Peta genangan untuk GIS eksternal |
| Visualisasi | **Kepler.gl** / web dashboard | Output 2 — populasi terdampak |
| Notifikasi | WhatsApp/SMS gateway (simulasi) | Output 1 — level siaga |

## Parameter streaming TMA (buku)

| Parameter | Nilai | Alasan |
|---|---|---|
| Window | 1 jam tumbling + slide 15 menit | Time of concentration DAS Musi 4–8 jam |
| Watermark | 30 menit | Toleransi data sensor terlambat |
| Topik Kafka | `sensor.tma.musi` | Satu topik per DAS (contoh) |

Ambang siaga TMA (stasiun referensi Kayu Agung, contoh buku):

| Level | TMA (cm) | Hujan kum. 3 jam (mm) |
|---|---|---|
| HIJAU | &lt; 650 | &lt; 30 |
| KUNING | 650–850 | 30–50 |
| ORANYE | 850–1020 | 50–80 |
| MERAH | &gt; 1020 | &gt; 80 |

## Port layanan (rencana lab)

> Sesuaikan jika bentrok dengan modul Bab 3–16. Konfirmasi di `docker-compose.yml` Lampiran.

| Layanan | Port (host) | UI / API |
|---|---|---|
| Kafka | 9092 | — |
| Spark UI | 4040 | Job streaming |
| MinIO API / Console | 9000 / 9001 | S3 + konsol |
| Airflow | 8080 | DAG batch |
| GeoServer | 8082 | WMS/WFS |
| Dashboard Kepler | 3001 atau static | Output 2 |

## Checklist Sprint 1 (infrastruktur)

- [ ] `docker compose up` — semua service healthy  
- [ ] Topik Kafka dibuat; producer simulasi TMA mengirim JSON  
- [ ] Bucket MinIO `geodata` / namespace Iceberg `banjir_musi`  
- [ ] Spark dapat membaca Bronze sample dari MinIO  
- [ ] Dokumentasi `.env.example` tanpa kredensial produksi  

## Checklist Sprint 2 (integrasi)

- [ ] Streaming job menulis agregat window ke Gold `tma_siaga`  
- [ ] DAG Airflow harian: ingest Sentinel-1 / update genangan  
- [ ] Sedona dapat `ST_Intersects` kelurahan × genangan  

## Checklist Sprint 3 (demo)

- [ ] End-to-end: sensor ORANYE → Gold terbaru → GeoJSON Kepler &lt; 5 menit (SLO)  
- [ ] Notifikasi uji ke channel simulasi  
- [ ] PDF logistik per shelter (template)  

## Keamanan dan etika

- Jangan commit API key BMKG, Copernicus, atau kredensial BPBD.  
- Data populasi per kelurahan: aggregat saja di demo; hindari identitas individu.  
- Simulasikan notifikasi massal hanya di lingkungan lab.  

## File terkait (repositori)

| Path | Fungsi |
|---|---|
| [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md) | Sumber data yang di-ingest |
| [../analitik/PANDUAN-ANALITIK.md](../analitik/PANDUAN-ANALITIK.md) | Job analitik |
| [../output/PANDUAN-OUTPUT.md](../output/PANDUAN-OUTPUT.md) | Deliverable akhir |
