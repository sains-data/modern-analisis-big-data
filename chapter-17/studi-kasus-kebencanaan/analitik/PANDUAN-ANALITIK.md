# Panduan Analitik — Peringatan Dini Banjir DAS Musi

## Pemetaan sprint ↔ analitik

| Sprint | User story (ringkas) | Folder analitik | Output downstream |
|---|---|---|---|
| 1 | Bronze lengkap + 3 pertanyaan & metrik | `batch/ingest_*`, dokumen metrik | `data/bronze/`, `data/silver/` awal |
| 2 | Streaming TMA + spatial join populasi | `streaming/tma_siaga.py`, `sql/populasi_terdampak.sql` | `data/gold/` |
| 2 | Prediksi TMA (opsional) | `model/lstm_tma/` | Gold forecast |
| 3 | Dasbor + routing | `sql/routing_shelter.sql`, export GeoJSON | [../output/](../output/) |

## 1. Streaming — agregasi sensor TMA

**Tujuan:** status siaga HIJAU / KUNING / ORANYE / MERAH setiap 15 menit.

Alur (dari buku):

1. Baca Kafka `sensor.tma.musi`  
2. Parse JSON: `stasiun_id`, `tma_cm`, `ts`  
3. `withWatermark("ts", "30 minutes")`  
4. `groupBy(window("ts", "60 minutes", "15 minutes"), stasiun_id)`  
5. Agregat: `max`, `avg`, `count` → kolom `siaga` dengan `when(tma_max_cm > …)`  

Nama file rencana: `analitik/streaming/tma_siaga_stream.py`

**Validasi:** bandingkan 1 event ORANYE dengan log manual BBWS (jika ada) atau skenario uji di Lampiran.

## 2. Batch — citra & geospasial statis

| Job | Input | Output Silver/Gold |
|---|---|---|
| `ingest_dem.py` | SRTM/DEMNAS | `silver.dem_musi` |
| `ingest_batas.py` | DAS, kelurahan GADM | `silver.kelurahan_sumsel` |
| `ingest_sentinel1.py` | GeoTIFF SAR | `silver.genangan_sar` → `gold.genangan_aktif` |
| `ingest_osm.py` | PBF jalan | `silver.jalan_evakuasi` |

Orkestrasi: DAG Airflow harian (citra 6 hari) + mingguan (OSM).

## 3. Spatial join — populasi terdampak

**Pertanyaan:** Siapa terdampak?

Logika inti (Sedona SQL, buku):

- Join `kelurahan_sumsel` × `genangan_aktif` pada `ST_Intersects`  
- Transform ke CRS metrik (mis. EPSG:32748) untuk `ST_Area` intersection  
- `estimasi_terdampak = jumlah_penduduk × (luas_intersect / luas_kelurahan)`  
- Filter `genangan.snapshot_ts` ≥ now() − 1 hour  

Nama file rencana: `analitik/sql/populasi_terdampak.sql`

**Metrik:** eksekusi &lt; 60 detik pada subset lab (ukuran disepakati tim).

## 4. Routing evakuasi — KNN join

**Pertanyaan:** Ke mana mengungsi?

- Input: titik populasi terdampak (atau centroid kelurahan), `silver.jalan`, `gold.shelter_kapasitas`  
- Constraint: jalan tidak memotong `genangan_aktif`  
- Algoritme: **KNN join** Sedona ke shelter terdekat  

Nama file rencana: `analitik/sql/routing_evakuasi.sql`

## 5. Prediksi TMA — LSTM (opsional)

**Pertanyaan:** Kapan banjir (6–12 jam ke depan)?

- Fitur: deret TMA + curah hujan kumulatif hulu  
- Model: LSTM (PyTorch/TensorFlow) — training batch offline, inferensi terjadwal atau streaming mini-batch  
- Tulis ke `gold.tma_forecast`  

Folder: `analitik/model/lstm_tma/`

## 6. Notifikasi (trigger analitik)

Saat `siaga IN ('ORANYE','MERAH')`:

1. Trigger micro-batch spatial join  
2. Refresh materialisasi `gold.populasi_terdampak`  
3. Publish event ke topik `alert.banjir.musi` (konsumen: notifikasi + Kepler export)  

## Physical plan (wajib Sprint 3)

Untuk setiap join spasial, tim wajib menyimpan cuplikan `df.explain()` di `analitik/docs/explain/`:

- Harapan: **RangeJoin** atau **BroadcastIndexJoin**  
- Hindari: **CartesianProduct** — jika muncul, perbaiki index/partisi (lihat Bab 16)  

## Product backlog lengkap

| Sprint | User story | Peran |
|---|---|---|
| 1 | Semua dataset di Bronze GeoParquet | Data Engineer |
| 1 | 3 pertanyaan analitik + metrik | Product Owner |
| 2 | Pipeline streaming TMA → Gold | Data Engineer |
| 2 | Spatial join populasi &lt; 60 dtk | Data Scientist |
| 3 | Dasbor Kepler.gl siaga + terdampak | BI Developer |
| 3 | Retrospective | Scrum Master |

## Rujukan kode di buku

Cuplikan referensi ada di `chapter-17.tex`:

- `programcode` agregasi Kafka + window Spark  
- `programcode` SQL estimasi populasi terdampak  
- `programcode` konfigurasi layer Kepler.gl (`kepler_config.py`)  

Salin ke repo saat Lampiran diterbitkan; jangan menggandakan di sini agar satu sumber kebenaran.
