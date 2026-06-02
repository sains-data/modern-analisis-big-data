# Panduan Output Sistem — Pemantauan KEL

Empat skala keputusan: taktis ranger → penegakan hukum → regulasi EUDR → perencanaan koridor jangka panjang.

---

## Output 1 — Peringatan dini konflik gajah–manusia

**Folder:** `output/output-1-alert-konflik/`

### Penerima

Grup WhatsApp **desa terdampak**; dashboard **BBKSDA** (topik `output.alert.konflik`).

### Frekuensi

**Real-time** — SLO **&lt; 5 menit** dari fix GPS.

### Isi pesan (contoh)

- Nama individu (mis. *Betina Dewasa Intan*)  
- Jarak ke desa terdekat (m)  
- Arah pergerakan  
- Rekomendasi (jauhi ternak, api pengusir)  

### Artefak

- Event Kafka / log `alert_konflik_*.jsonl`  
- Cuplikan pesan WhatsApp simulasi  

### Sumber

Streaming `gps.collar.leuser` + `bronze.permukiman_sekitar_kel`.

---

## Output 2 — Bukti deforestasi real-time

**Folder:** `output/output-2-bukti-deforestasi/`

### Penerima

**KLHK**, tim **penegakan hukum** BBKSDA.

### Frekuensi

**Harian** (setelah pemrosesan tile Sentinel-2).

### Isi

- Peta sel/piksel deforestasi aktif (ΔNDVI)  
- Koordinat + luas estimasi  
- Timestamp deteksi  

### Artefak

- `deforestasi_YYYYMMDD.geojson`  
- Layer WMS opsional (GeoServer)  

### Sumber

`gold.deforestasi_aktif`.

---

## Output 3 — Laporan monitoring KEL (EUDR)

**Folder:** `output/output-3-laporan-kel-eudr/`

### Penerima

Pelaporan regulasi **EUDR** (Komisi Eropa) — kompatibilitas rantai pasok.

### Frekuensi

**Bulanan**.

### Isi

- Ringkasan luas deforestasi dalam / dekat KEL  
- Hotspot tekanan tertinggi  
- Status patroli vs coverage gap  
- Metadata format kompatibel **Global Forest Watch API** (validasi Sprint 3)  

### Artefak

- `laporan_kel_YYYYMM.pdf`  
- `monitoring_kel_YYYYMM.geojson`  

---

## Output 4 — Basis data pergerakan satwa

**Folder:** `output/output-4-basis-pergerakan/`

### Penerima

**Riset** universitas mitra FKL; perencanaan **koridor hijau**.

### Frekuensi

**Akumulatif** (arsip tahunan).

### Isi

- Trajektori GPS per individu (terbatas/teranonimisasi untuk publikasi)  
- Poligon home range 50% / 95%  
- Indeks konektivitas habitat (least-cost path)  

### Artefak

- `home_range_{individu_id}.geojson`  
- `pergerakan_harian.parquet` (akses terkontrol)  

### Etika

Jangan publikasikan koordinat presisi satwa terancam di repo terbuka.

---

## Matriks output × pertanyaan analitik

| Pertanyaan | Output |
|---|---|
| Deforestasi aktif? | Output 2, 3 |
| Home range & konsesi? | Output 4 |
| Potensi konflik? | Output 1 (+ Gi* di analitik) |
| Prioritas patroli? | Output 3 + GPX rute (Sprint 3) |

---

## Checklist presentasi Sprint 3

- [ ] Simulasi 1 alert gajah &lt; 5 menit  
- [ ] GPX rute patroli unduh di peta  
- [ ] PDF + GeoJSON lolos checklist format GFW  
- [ ] Diskusi edge vs cloud dan privasi GPS  

---

## Lampiran

Skrip `output_01` … dan konfigurasi dashboard ranger di Lampiran Bab 17.
