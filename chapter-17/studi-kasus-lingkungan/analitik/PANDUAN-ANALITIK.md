# Panduan Analitik — Monitoring Karhutla Riau

## Pemetaan sprint ↔ analitik

| Sprint | Fokus | Artefak |
|---|---|---|
| 1 | Bronze + definisi \(I_{\text{risiko}}\) | `data/bronze/`, dokumen bobot |
| 2 | DAG batch + streaming + join | `gold.indeks_risiko_karhutla`, `gold.rekam_hotspot_terverifikasi` |
| 2 | Korelasi ISPU–ISPA | `gold.korelasi_ispu_ispa`, `gold.lag_optimal_kecamatan` |
| 3 | Export output + dasbor | [../output/](../output/) |

## 1. Batch — Sentinel-2 NBR/NDVI

**Task:** `kalkulasi_nbr`

- Input: `bronze.sentinel2` multi-band  
- Sedona `RS_MapAlgebra` → NDVI, NBR  
- Output: `silver.ndvi_nbr`  
- Jadwal: setelah tile tersedia (~02:00 WIB)

## 2. Batch — Join spasial akuntabilitas

**Task:** `join_spasial`

```sql
-- Pola inti (buku): hotspot terverifikasi dalam konsesi
SELECT k.nama_perusahaan, k.no_izin, COUNT(h.hotspot_id) AS n_hotspot, ...
FROM konsesi_riau k
JOIN hotspot_firms_verified h ON ST_Contains(k.geom, h.geom)
WHERE h.confidence IN ('nominal', 'high')
GROUP BY ...
ORDER BY n_hotspot DESC;
```

- Presisi: `ST_Contains` (titik dalam poligon konsesi)  
- Filter tambahan: overlap peta **gambut** untuk verifikasi karhutla gambut  
- File rencana: `analitik/sql/akuntabilitas_konsesi.sql`

**Validasi:** `explain()` — hindari CartesianProduct; pastikan index/spatial partition.

## 3. Batch — Indeks risiko karhutla

**Task:** `indeks_risiko`

1. Agregat komponen \(G, F, H, N, D\) per `h3_id`  
2. Hitung \(I_{\text{risiko}}\) (bobot buku)  
3. Tulis `gold.indeks_risiko_karhutla` partition `tanggal=`

Klasifikasi 5 kelas untuk output: Sangat Rendah … Sangat Tinggi (0–0.2 … 0.8–1.0).

## 4. Streaming — FIRMS ke H3

- Topik: `hotspot.firms.riau`  
- Window: tumbling **harian**  
- Agregat: `count`, `sum(frp)` per `h3_id` resolusi **7**  
- File rencana: `analitik/streaming/firms_h3_daily.py`

## 5. Streaming — ISPA & korelasi lag

- Topik: `ispa.kecamatan.riau`  
- Window: sliding **7 hari**  
- Batch/stream gabung ISPU harian  
- CCF / `F.corr` untuk lag 0–7 hari per kecamatan  
- File rencana: `analitik/batch/korelasi_ispu_ispa.py` (cuplikan: `output_03_ispu_ispa.py` di buku)

## 6. Analitik lanjutan (opsional sprint 2+)

| Teknik | Tujuan |
|---|---|
| **Getis-Ord Gi*** | Klaster hotspot berulang |
| **XGBoost** | Prediksi risiko 3 hari ke depan |
| **Moran's I** | Autokorelasi spasial dampak ISPA |

## 7. Emisi karbon (menuju Output 4)

- Burned area dari FRP: contoh buku **1 MW FRP ≈ 0,3 ha** gambut  
- Faktor emisi IPCC Tier 1 per tipe/kedalaman gambut  
- File rencana: `analitik/sql/emisi_karbon_ipcc.sql`

## Product backlog (ringkas)

| Sprint | User story | Peran |
|---|---|---|
| 1 | Semua dataset Bronze + skema valid | Data Engineer |
| 1 | Formula indeks risiko disetujui | Product Owner |
| 2 | DAG Airflow harian → Gold indeks risiko | Data Engineer |
| 2 | Akuntabilitas &lt; 60 dtk | Data Scientist |
| 2 | Korelasi lag ISPU–ISPA | Data Scientist |
| 3 | Dasbor Kepler + filter tanggal | BI Developer |
| 3 | Retrospective | Scrum Master |

## Rujukan kode di buku

- `output_01_peta_risiko.py` — ekspor GeoJSON + WhatsApp  
- `output_02_akuntabilitas.py` — PDF bulanan KLHK/KPK  
- `output_03_ispu_ispa.py` — korelasi lag → Superset  
- `output_04_emisi_karbon.py` — IPCC Tier 1  

Implementasi menyusul di Lampiran; logika mengacu cuplikan di `chapter-17.tex`.
