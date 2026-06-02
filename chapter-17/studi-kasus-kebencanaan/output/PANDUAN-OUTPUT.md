# Panduan Output Sistem — Peringatan Dini Banjir DAS Musi

Empat output di bawah ini merujuk **Gambar empat output** dan subbab *Output Sistem dan Impak Kebijakan* pada `chapter-17.tex` §Studi Kasus Kebencanaan.

---

## Output 1 — Level peringatan otomatis

**Folder:** `output/output-1-level-siaga/`

### Isi artefak

| File (contoh) | Format | Deskripsi |
|---|---|---|
| `alert_YYYYMMDD_HHMM.json` | JSON | Event: stasiun, TMA, siaga, hujan 3 jam |
| `notifikasi_template.txt` | Teks | Template WhatsApp untuk operator |

### Trigger

- Kombinasi **TMA** (stasiun Kayu Agung) + **curah hujan kumulatif 3 jam** hulu  
- Level: HIJAU / KUNING / ORANYE / MERAH — lihat Tabel ambang di [PANDUAN-ARSITEKTUR-LAB.md](../arsitektur-lab/PANDUAN-ARSITEKTUR-LAB.md)

### Tindakan operasional (ringkas)

| Level | Contoh tindakan BPBD |
|---|---|
| KUNING | Siaga tim, informasi lurah/RW |
| ORANYE | Evakuasi preventif zona rendah, aktifkan posko |
| MERAH | Evakuasi masif, tutup jalan terdampak |

### Sumber data

`data/gold/tma_siaga_hourly` + agregat hujan BMKG Silver.

---

## Output 2 — Peta sebaran populasi terdampak

**Folder:** `output/output-2-peta-terdampak/`

### SLO

**≤ 5 menit** dari sensor melewati ambang ORANYE/MERAH hingga peta terbaru di dasbor.

### Timeline target (buku)

| Waktu | Kejadian |
|---|---|
| t+0 | Sensor melewati ambang (mis. 850 cm) |
| t+15 dtk | Kafka menerima event |
| t+30 dtk | Spark micro-batch |
| t+45 dtk | Spatial join selesai |
| t+60 dtk | Gold diperbarui |
| t+5 menit | Kepler.gl menampilkan layer |

### Artefak

| File | Format |
|---|---|
| `terdampak_*.geojson` | GeoJSON kelurahan + `estimasi_terdampak` |
| `sensor_tma_*.geojson` | Titik sensor + `siaga` |
| `genangan_*.geojson` | Poligon genangan aktif |
| `kepler_config.json` | Konfigurasi layer (choropleth, sensor, genangan) |

### Layer Kepler (tiga lapisan)

1. **Choropleth** kelurahan — field `estimasi_terdampak`, palet merah  
2. **Point** sensor TMA — warna per `siaga_order` (0–3)  
3. **Polygon** genangan aktif — semi-transparan  

Referensi struktur JSON: `kepler_config.py` di buku.

---

## Output 3 — Rencana distribusi logistik

**Folder:** `output/output-3-logistik/`

### Isi

PDF otomatis **per titik shelter** berisi:

- Nama shelter, kapasitas, okupansi estimasi  
- Rute akses dari kecamatan terdampak utama  
- Kebutuhan logistik dasar (air, tenda, pangan — parameter tim)  

### Sumber analitik

- `analitik/sql/routing_evakuasi.sql`  
- `data/gold/shelter_kapasitas` + `gold.populasi_terdampak`

### Format

- `logistik_shelter_<id>_<tanggal>.pdf`  
- Ringkasan agregat: `logistik_ringkasan_<tanggal>.pdf`

---

## Output 4 — Laporan after-action

**Folder:** `output/output-4-after-action/`

### Tujuan

Evaluasi respons pasca-kejadian untuk **BNPB / manajemen** — bukan untuk operasi per menit.

### Bab yang disarankan

1. **Ringkasan kejadian** — timeline sensor, puncak TMA, luas genangan  
2. **Kinerja sistem** — apakah SLO 5 menit terpenuhi; false alarm  
3. **Dampak** — total `estimasi_terdampak` vs lapangan (jika ada)  
4. **Lessons learned** — retrospective Scrum sprint 1–3  
5. **Rekomendasi** — sensor tambahan, perbaikan ambang, data WorldPop  

### Format

- `after_action_YYYYMMDD.pdf` atau `.md` untuk versi draft tim  

---

## Matriks output × pertanyaan analitik

| Pertanyaan | Output utama | Output pendukung |
|---|---|---|
| Kapan? | Output 1 (siaga + prediksi) | Output 4 (timeline) |
| Siapa? | Output 2 (peta terdampak) | Output 1 (notifikasi wilayah) |
| Ke mana? | Output 3 (logistik shelter) | Output 2 (layer shelter di peta) |

---

## Checklist presentasi akhir

- [ ] Simulasi 1 skenario MERAH end-to-end direkam (screencast atau log)  
- [ ] Empat folder berisi minimal 1 file contoh masing-masing  
- [ ] Penjelasan 5 menit untuk audiens non-teknis (Bahasa Indonesia)  
- [ ] Diskusi keterbatasan estimasi populasi proporsional  

---

## Lampiran

Template PDF, webhook notifikasi simulasi, dan skrip export GeoJSON akan disertakan di **Lampiran** praktikum Bab 17.
