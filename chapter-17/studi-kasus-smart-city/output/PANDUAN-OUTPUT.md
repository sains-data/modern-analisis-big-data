# Panduan Output Sistem — Kota Medan

Keempat output saling mengisi: kurangi macet → turunkan emisi → perbaiki udara yang dipantau warga.

---

## Output 1 — Dashboard ATCS

**Folder:** `output/output-1-atcs/`

### Penerima

**Dishub** — operator 120 persimpangan.

### Frekuensi

**Real-time** — peta diperbarui ~**15 detik**; SLO rekomendasi rute **&lt;5 menit** setelah macet.

### Fitur

- Peta ruas: hijau / kuning / merah (LANCAR/PADAT/MACET)  
- Ubah durasi fase lampu (persimpangan terhubung)  
- **Rekomendasi rute alternatif** otomatis saat koridor MACET  

### Artefak

- Feed Kafka `output.kondisi.jalan`  
- Layer GeoJSON / tile untuk Superset/Kepler  
- Log rekomendasi rute `rute_alternatif_*.json`  

### Sumber

`output_01_atcs_dashboard.py` — join `gold.lalu_lintas` + geometri OSM.

---

## Output 2 — IQU hiperlokal untuk warga

**Folder:** `output/output-2-iqu-hiperlokal/`

### Penerima

**Masyarakat** — aplikasi publik (tanpa login atau SSO kota).

### Frekuensi

**Per 10 menit** — grid **500 m**.

### Isi

- PM₂.₅ interpolasi + kategori **ISPU**  
- Peta heatmap per kelurahan/kecamatan (filter)  
- Peringatan saat ISPU tidak sehat  

### Artefak

- `iqu_grid_YYYYMMDDHHMM.geojson`  
- API JSON ringan (Lampiran)  

### Sumber

`gold.kualitas_udara` (IDW + angin).

---

## Output 3 — Optimasi rute Trans Metro Deli

**Folder:** `output/output-3-optimasi-tmd/`

### Penerima

**Dishub** + **operator TMD**.

### Frekuensi

**Bulanan** (revisi rute/headway).

### Isi

- Daftar kelurahan **underserved** (coverage &lt;30%, 400 m)  
- Rekomendasi perpanjangan rute, frekuensi headway, lokasi halte baru  
- Peta gap vs permintaan  

### Artefak

- `rekomendasi_tmd_YYYYMM.pdf`  
- `gap_kelurahan_YYYYMM.csv`  

### Sumber

`gold.gap_tmd_kelurahan`, analitik `gap_tmd`.

---

## Output 4 — Laporan emisi kendaraan

**Folder:** `output/output-4-laporan-emisi/`

### Penerima

**DLH Kota Medan**, **KLHK** — dasar kebijakan pembatasan kendaraan / zonasi.

### Frekuensi

**Bulanan**.

### Isi

- Emisi CO₂, NOₓ, PM₂.₅ per **kecamatan**  
- Korelasi dengan volume & kecepatan rata-rata  
- Narasi untuk rapat Bappeda  

### Artefak

- `emisi_kecamatan_YYYYMM.pdf`  
- `emisi_kecamatan_YYYYMM.csv`  

### Sumber

`gold.emisi` — batch `estimasi_emisi`.

---

## Matriks output × pertanyaan analitik

| Pertanyaan | Output |
|---|---|
| Hotspot kemacetan? | Output 1 (+ Gi* analitik) |
| Korelasi PM₂.₅–volume? | Output 2, 4; `gold.korelasi_pm25` |
| Gap layanan TMD? | Output 3 |

---

## Checklist Sprint 3

- [ ] Demo ATCS ke Dishub + DLH (filter kecamatan)  
- [ ] Cuplikan IQU 500 m di peta warga  
- [ ] PDF emisi + CSV valid  
- [ ] Dua pertanyaan klien terjawab dengan query Gold  
- [ ] Retrospective: satu perbaikan proses konkret  

---

## Lampiran

Skrip output, dashboard Superset, dan producer Kafka di Lampiran Bab 17.
