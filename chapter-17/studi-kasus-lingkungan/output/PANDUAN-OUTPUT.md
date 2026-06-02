# Panduan Output Sistem — Monitoring Karhutla Riau

Empat output merujuk Gambar output karhutla dan subbab *Output Sistem dan Impak Kebijakan* (`chapter-17.tex` §Studi Kasus Lingkungan).

---

## Output 1 — Peta risiko harian

**Folder:** `output/output-1-peta-risiko/`

### Penerima

BPBD kabupaten/kota — grup WhatsApp Pusdalops.

### Frekuensi

**Harian**, dikirim **06:00 WIB** (task Airflow ~05:45 WIB).

### Artefak

| File | Format |
|---|---|
| `peta_risiko_YYYY-MM-DD.geojson` | H3 hex + `indeks`, `kelas_risiko`, `warna_hex` |
| `peta_risiko_YYYY-MM-DD.png` | Snapshot peta |
| `ringkasan_whatsapp.txt` | Jumlah sel Tinggi / Sangat Tinggi |

### Kelas risiko (Tabel 17 kelas risiko)

| Kelas | Nilai \(I\) | Warna | Tindakan BPBD (ringkas) |
|---|---|---|---|
| Sangat Rendah | 0,0–0,2 | Abu-abu | Pemantauan rutin |
| Rendah | 0,2–0,4 | Hijau | Siaga MPA |
| Sedang | 0,4–0,6 | Kuning | Patroli, cek kanal gambut |
| Tinggi | 0,6–0,8 | Oranye | Manggala Agni, larangan bakar |
| Sangat Tinggi | 0,8–1,0 | Merah | Siaga darurat lintas instansi |

Layer tambahan: titik panas aktif **24 jam** terakhir.

### Sumber

`gold.indeks_risiko_karhutla`, FIRMS streaming.

---

## Output 2 — Laporan akuntabilitas konsesi

**Folder:** `output/output-2-akuntabilitas-konsesi/`

### Penerima

**KLHK** (SIGAP) dan **KPK** — bukti hukum PP 71/2014.

### Frekuensi

**Bulanan** (tanggal 1).

### Isi laporan

- `nama_perusahaan`, `no_izin`, `jenis_konsesi`  
- `n_hotspot`, `total_frp_mw`, `n_hari_aktif`  
- Estimasi **luas terbakar** (FRP → ha, faktor 0,3 ha/MW contoh buku)  
- Status **kepatuhan** (MEMENUHI / MELANGGAR)  

### Artefak

| File | Format |
|---|---|
| `akuntabilitas_YYYY-MM.pdf` | PDF bertanda tangan digital |
| `akuntabilitas_YYYY-MM.csv` | Tabel agregat untuk audit |

### Sumber

`gold.rekam_hotspot_terverifikasi`, query `ST_Contains` konsesi.

---

## Output 3 — Dashboard publik ISPU–ISPA

**Folder:** `output/output-3-dashboard-ispu-ispa/`

### Penerima

Masyarakat, jurnalis, organisasi kesehatan — **tanpa autentikasi**.

### Frekuensi

**Mingguan**.

### Visualisasi

- Scatter ISPU vs kunjungan ISPA  
- Time series per kecamatan  
- Highlight kecamatan dengan **lag optimal** dan korelasi ≥ 0,5  

### Artefak

- Dataset Superset: `gold.korelasi_ispu_ispa`, `gold.lag_optimal_kecamatan`  
- Export JSON konfigurasi dashboard (Lampiran)  

### Sumber analitik

`output_03_ispu_ispa.py` — lag 0–7 hari, Pearson per kecamatan.

---

## Output 4 — Estimasi emisi karbon (NDC)

**Folder:** `output/output-4-emisi-karbon/`

### Penerima

Pelaporan **NDC Indonesia** ke UNFCCC; komunitas iklim internasional.

### Frekuensi

**Per kejadian** kebakaran besar (dan agregat tahunan opsional).

### Metode

- **IPCC Tier 1**: burned area × emission factor per tipe/kedalaman gambut  
- Referensi: van der Werf et al. (2017), Wetlands Supplement  

### Artefak

| File | Isi |
|---|---|
| `emisi_per_konsesi_YYYYMMDD.csv` | Ton CO₂e per konsesi |
| `emisi_ringkasan_kejadian.pdf` | Narasi metodologi + total |

### Sumber

`gold.emisi_karbon_konsesi`, join hotspot–konsesi–gambut.

---

## Matriks output × pertanyaan analitik

| Pertanyaan | Output utama | Pendukung |
|---|---|---|
| Di mana risiko? | Output 1 | Gold indeks risiko |
| Konsesi mana? | Output 2 | Join akuntabilitas |
| Emisi & kesehatan? | Output 4, Output 3 | Emisi IPCC; korelasi ISPA |

---

## Checklist presentasi Sprint 3

- [ ] Demo peta risiko dengan filter tanggal di Kepler  
- [ ] Cuplikan PDF akuntabilitas 1 bulan (data sintetis)  
- [ ] Dashboard ISPU–ISPA dengan ≥1 kecamatan korelasi tinggi  
- [ ] Tabel emisi contoh untuk 1 kejadian  
- [ ] Diskusi limitasi FRP→ha dan asumsi Tier 1  

---

## Lampiran

Skrip `output_01` … `output_04` dari buku akan ditempatkan di Lampiran praktikum Bab 17.
