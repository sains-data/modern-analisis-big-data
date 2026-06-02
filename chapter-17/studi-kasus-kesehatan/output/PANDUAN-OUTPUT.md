# Panduan Output Sistem — Analitik Stunting Sumatera Utara

Merujuk Gambar output stunting (`chapter-17.tex` §Studi Kasus Kesehatan).

---

## Output 1 — Peta prioritas 50 desa per kabupaten

**Folder:** `output/output-1-prioritas-desa/`

### Penerima

Bupati, kepala Dinkes — alokasi **Dana Desa** (satuan kabupaten).

### Frekuensi

**Bulanan** (Airflow tanggal **5**).

### Isi

| Kolom | Makna |
|---|---|
| `rank_kabupaten` | Peringkat 1–50 dalam kabupaten |
| `indeks_total` | Skor risiko multifaktor |
| `d1`…`d5` | Lima dimensi (prevalensi, sanitasi, kemiskinan, akses, air) |
| `prev_pct` | Prevalensi stunting aktual (%) |
| `waktu_tempuh_menit` | Ke Puskesmas terdekat |
| `status` | `BARU` / `KRONIS` (3 bulan prioritas berturut) |

### Artefak

- `prioritas_desa_YYYYMM.csv` / Parquet  
- Peta choropleth desa (GeoJSON) opsional  

### Sumber

`gold.indeks_risiko_stunting_multifaktor`, `gold.prioritas_desa_bulanan`.

---

## Output 2 — Dashboard TPPS Provinsi Sumatera Utara

**Folder:** `output/output-2-dashboard-tpps/`

### Penerima

**TPPS** — rapat koordinasi 33 kab/kota.

### Frekuensi

**Mingguan** (data agregat); panel tren bulanan diperbarui tiap siklus Posyandu.

### Empat panel (buku)

1. **Tren provinsi** — prevalensi 12 bulan vs target **14%**  
2. **Peta kabupaten** — choropleth + drill-down desa  
3. **Top 10 desa terburuk** — tabel otomatis  
4. **Aksesibilitas** — isokron 30/60/90 menit, blank zone  

### Artefak

- Dataset Parquet di `gold/dashboard/` (tren, kab, akses)  
- `stunting_kab_bulan_ini.geojson`  
- Dashboard **Apache Superset** (konfigurasi Lampiran)  
- **Ekspor PDF** untuk rapat (Sprint 3 DoD)  

### Sumber

`output_02_dashboard_tpps.py` (buku).

---

## Output 3 — Alert kader Posyandu

**Folder:** `output/output-3-alert-kader/`

### Penerima

**Kader Posyandu** (aplikasi mobile / WhatsApp simulasi).

### Frekuensi

**Real-time** (&lt; 30 detik).

### Jenis alert (Tabel 17 alert kader)

| Level | Pemicu | Tindak lanjut |
|---|---|---|
| MERAH | ΔBB &gt; 200 g/bln atau z &lt; −3 | Kunjungan 24 jam, rujuk Puskesmas |
| ORANYE | Turun z &gt; 0,5 SD atau absen 2 bln | Kunjungan 72 jam, edukasi gizi |
| KUNING | z −2 s.d. −1,5 | Pemantauan, PMT |

### Artefak

- Event Kafka `output.alert.kader`  
- Log uji: `alert_log_YYYYMMDD.jsonl`  

---

## Output 4 — Basis bukti pengusulan tenaga kesehatan

**Folder:** `output/output-4-bukti-nakes/`

### Penerima

**Bappeda** Provinsi Sumut, **Kementerian Kesehatan**.

### Frekuensi

**Triwulanan**.

### Indikator kunci

**Skor Kebutuhan Tenaga Kesehatan** per desa:

- Prevalensi stunting  
- Waktu tempuh ke fasilitas  
- Rasio balita per bidan  
- Ketersediaan kader aktif  

### Artefak

- `laporan_nakes_YYYYQ.pdf`  
- Tabel desa terpencil prioritas penempatan nakes  

---

## Matriks output × pertanyaan analitik

| Pertanyaan | Output utama |
|---|---|
| Klaster desa? | Output 1 + analitik DBSCAN |
| Faktor dominan? | Output 2 (panel) + regresi (notebook) |
| Aksesibilitas? | Output 2 panel 4, Output 4 |

---

## Checklist presentasi Sprint 3

- [ ] Demo TPPS: filter kabupaten + ekspor PDF  
- [ ] GeoJSON isokron 3 zona valid  
- [ ] Simulasi 1 alert MERAH end-to-end  
- [ ] Daftar 50 desa contoh 1 kabupaten dengan 5 dimensi  
- [ ] Diskusi privasi data balita  

---

## Lampiran

Skrip `output_01` … `output_04` dan dashboard Superset menyusul di Lampiran Bab 17.
