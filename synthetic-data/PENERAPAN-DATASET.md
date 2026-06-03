# Penerapan Sintesis Copula pada Dataset Praktikum

Dokumen ini mendeskripsikan **bagaimana metode Gaussian Copula diterapkan** untuk menghasilkan data sintesis seragam lintas modul praktikum. Penjelasan menggunakan istilah netral (*entitas partisipan*, *catatan aktivitas*, *unit layanan*) tanpa merujuk label domain industri tertentu.

---

## 1. Tujuan penerapan

| Tujuan | Deskripsi |
|--------|-----------|
| **Konsistensi schema** | Kolom dan tipe data sama dari modul pengenalan data lake hingga pipeline end-to-end |
| **Konsistensi statistik** | Korelasi nominal–frekuensi–lokasi–saluran terjaga di semua volume |
| **Skala progresif** | 7 → 15 → 500 → 10.000 → 15.000 baris tanpa mengubah definisi variabel |
| **Anomali terkontrol** | Modul data quality menerima subset baris dengan cacat yang dapat direproduksi |
| **Reproduksibilitas lab** | Seed tetap; output identik di setiap mesin peserta |

---

## 2. Model entitas

Sistem data sintesis dibangun dari **empat entitas** yang saling berelasi:

```
┌─────────────────────┐       ┌──────────────────────────┐
│  Entitas Partisipan │◄──────│  Catatan Aktivitas       │
│  (master profil)    │  1:N  │  (event transaksional)   │
└─────────────────────┘       └────────────┬─────────────┘
                                           │
                              ┌────────────▼─────────────┐
                              │  Unit Layanan (penyedia) │
                              └──────────────────────────┘

┌─────────────────────┐       ┌──────────────────────────┐
│  Skor Kompetensi    │       │  Pembacaan Sensor        │
│  (modul analitik    │       │  (modul streaming)       │
│   dasar)            │       │                          │
└─────────────────────┘       └──────────────────────────┘
```

### 2.1 Entitas Partisipan

Profil individu atau organisasi yang terdaftar pada platform.

| Kolom | Tipe | Peran dalam copula |
|-------|------|-------------------|
| `id_partisipan` | string (PK) | Post-generate; tidak di-copula |
| `nama` | string | Lookup dari pool nama; tidak di-copula |
| `tipe_partisipan` | kategorik | PMF empiris → inverse CDF diskrit |
| `unit_geografis` | kategorik | PMF empiris; berkorelasi dengan nominal rata-rata |
| `segmen` | ordinal (1–3) | Via copula sebagai integer, lalu map ke label |
| `tanggal_bergabung` | tanggal | Offset numerik; korelasi dengan recency |
| `email` | string | Derivasi deterministik dari id; tidak di-copula |

### 2.2 Catatan Aktivitas

Event transaksional — inti dataset di sebagian besar modul.

| Kolom | Tipe | Peran dalam copula |
|-------|------|-------------------|
| `id_aktivitas` | string (PK) | Post-generate |
| `id_partisipan` | string (FK) | Sampling dari master partisipan |
| `id_unit_layanan` | string (FK) | Sampling weighted by unit geografis |
| `tanggal` / `event_time` | datetime | Numerik (epoch offset) dalam $\Sigma$ |
| `kelas_layanan` | kategorik | 6 kelas; korelasi dengan nominal |
| `nama_item` | string | Lookup per kelas; tidak di-copula |
| `saluran` | kategorik | 4–5 saluran interaksi |
| `kuantitas` | integer | Discrete via round setelah copula |
| `harga_satuan` | float | Log-transform → copula → exp inverse |
| `rasio_penyesuaian` | float [0, 0.3] | Beta-like marginal; clip setelah sample |
| `nilai_total` | float | **Derived**: `kuantitas × harga_satuan × (1 - rasio)` |
| `berat_unit` | float | Copula dengan kuantitas (logistik) |
| `unit_geografis` | kategorik | Consistent dengan partisipan atau independent draw |
| `status` | kategorik | `sukses`, `pending`, `gagal` — dominan sukses |

> **Catatan desain:** `nilai_total` dapat di-generate langsung dalam copula *atau* dihitung ulang setelah sampling komponennya. Pendekatan lab: **hitung ulang** agar constraint aritmetika selalu terpenuhi.

### 2.3 Unit Layanan

Penyedia layanan yang menerima aktivitas.

| Kolom | Tipe |
|-------|------|
| `id_unit` | string (PK) |
| `nama_unit` | string |
| `kelas_layanan` | kategorik |
| `unit_geografis` | kategorik |
| `skala_operasi` | ordinal |

### 2.4 Skor Kompetensi

Digunakan modul analitik dasar (pengganti dataset akademik terpisah).

| Kolom | Tipe |
|-------|------|
| `id_partisipan` | FK |
| `skor_modul_a` | float [0, 100] |
| `skor_modul_b` | float [0, 100] |
| `skor_modul_c` | float [0, 100] |

Ketiga skor di-generate **bersama-sama** via Gaussian Copula 3D dengan $\Sigma$ positif (skor saling berkorelasi moderat).

### 2.5 Pembacaan Sensor

Event streaming untuk modul aliran data.

| Kolom | Tipe |
|-------|------|
| `event_id` | string |
| `sensor_id` | string |
| `lokasi` | kategorik (5 lokasi fasilitas) |
| `suhu` | float |
| `kelembapan` | float |
| `status` | kategorik (`normal`, `warning`, `critical`) |

Pasangan `(suhu, kelembapan)` di-generate via copula bivariat; `status` diturunkan dari threshold suhu/kelembapan.

---

## 3. Blok variabel untuk estimasi $\Sigma$

Copula dijalankan per **blok** agar estimasi stabil:

### Blok A — Profil partisipan (master, $n \approx 300$)

| Variabel masuk $\Sigma$ | Transformasi |
|-------------------------|--------------|
| `tipe_partisipan` (encoded) | Uniform pseudo |
| `unit_geografis` (encoded) | Uniform pseudo |
| `segmen` (1–3) | Integer |
| `offset_bergabung` (hari) | Numerik |

### Blok B — Catatan aktivitas (core, $n$ = 500 – 15.000)

| Variabel masuk $\Sigma$ | Transformasi |
|-------------------------|--------------|
| `log_harga_satuan` | Log |
| `kuantitas` | Numerik → round |
| `rasio_penyesuaian` | Beta / uniform |
| `offset_waktu` | Numerik |
| `kelas_layanan` (encoded) | Uniform pseudo |
| `saluran` (encoded) | Uniform pseudo |
| `berat_unit` | Log |

Matriks korelasi target (contoh struktur, nilai final dari data referensi):

|  | log_harga | kuantitas | rasio | offset_waktu |
|--|-----------|-----------|-------|--------------|
| log_harga | 1.00 | −0.15 | +0.10 | 0.00 |
| kuantitas | −0.15 | 1.00 | +0.05 | +0.08 |
| rasio | +0.10 | +0.05 | 1.00 | −0.05 |
| offset_waktu | 0.00 | +0.08 | −0.05 | 1.00 |

### Blok C — Sensor bivariat

| Variabel | Korelasi target |
|----------|-----------------|
| suhu ↔ kelembapan | +0.4 (moderat positif) |

---

## 4. Prosedur sintesis end-to-end

```
1. Generate master Entitas Partisipan (Blok A)
         │
2. Generate master Unit Layanan (PMF independen per kelas × geografis)
         │
3. Generate Catatan Aktivitas (Blok B)
   ├── Sample Z* ~ N(0, Σ_B)
   ├── Inverse marginal → komponen numerik & kategorik
   ├── Assign FK ke partisipan & unit (weighted sampling)
   ├── Hitung nilai_total
   └── Generate PK unik
         │
4. (Opsional) Injeksi anomali untuk modul data quality
         │
5. Derive agregat Gold (tren bulanan, per kelas, per geografis, RFM)
         │
6. Export format per modul (CSV, JSON, Parquet)
```

### 4.1 Weighted FK assignment

Setelah baris aktivitas disample, `id_partisipan` dipilih dengan probabilitas proporsional frekuensi aktivitas historis partisipan (zipf-like: sedikit partisipan high-volume, banyak partisipan low-volume). Ini **tidak** bagian dari copula, tetapi applied setelah sampling agar distribusi frekuensi realistis.

### 4.2 Anomali terkontrol (modul Bab 6–7)

| Anomali | Proporsi | Cara injeksi |
|---------|----------|--------------|
| Duplikat `id_aktivitas` | 1 baris | Copy baris + same PK |
| FK kosong | 1 baris | Null `id_partisipan` |
| Nilai negatif | 1 baris | Override `nilai_total` |
| Kuantitas nol | 1 baris | Override `kuantitas = 0` |
| Inkonsistensi geografis | 1 baris | Override casing `unit_geografis` |

Anomali di-inject **setelah** copula sampling agar modul cleaning memiliki input yang deterministis.

---

## 5. Pemetaan output per modul praktikum

Volume dan subset kolom disesuaikan per modul; **definisi kolom kanonik tidak berubah**.

| Modul | Entitas | Volume | Kolom / format | Anomali |
|-------|---------|--------|----------------|---------|
| Pengenalan data lake (MinIO) | Partisipan (subset profil) | 50–100 | `id`, `nama`, `usia`, `unit_geografis`, `pendapatan`, `tanggal_bergabung` | Duplikat + null |
| Analitik dasar (Spark intro) | Skor kompetensi | 10–20 | 3 skor + id + nama | — |
| Medallion pengenalan | Aktivitas + Partisipan | 15 + 7 | Schema penuh | Ya |
| Medallion lokal (Arrow) | Aktivitas + Partisipan | 15 + 7 | Schema penuh | Ya |
| Penyimpanan terdistribusi | Aktivitas + Partisipan | 500 + 50 | Tanpa `produk` detail; `nilai_total` langsung | Tidak |
| Orkestrasi harian | Aktivitas (generate/run) | 100/hari | Subset: `id`, `nilai_total`, `kelas_layanan` | ~3% bad rows |
| Streaming | Aktivitas (JSON) + Sensor | 100 seed + stream | `event_id`, `user_id`, `product`, `channel`, `amount`, `event_time` | Duplikat test set |
| Machine learning | Aktivitas silver | 10.000 | Schema ML + label `segmen` derived | Tidak |
| Visualisasi | Aktivitas silver + Gold | 15.000 + agregat | + partisi `tahun`, `bulan` | Tidak |
| Pipeline E2E | Silver + Gold + RFM | 15.000 | + `segmentasi_rfm` | Tidak |

> Kolom legacy (`user_id`, `product`, `amount`) pada modul streaming tetap didukung via **alias mapping** dari schema kanonik agar kode lab existing tidak perlu dirombak total.

### 5.1 Alias mapping (streaming)

| Kolom kanonik | Alias modul streaming |
|---------------|----------------------|
| `id_partisipan` | `user_id` |
| `kelas_layanan` | `product` |
| `nilai_total` | `amount` |
| `saluran` | `channel` |
| `event_time` | `event_time` |

---

## 6. Derivasi label dan agregat Gold

### 6.1 Label segmen (modul ML)

Dari `nilai_total` per baris:

| Segmen | Rule |
|--------|------|
| rendah | `< 100.000` |
| menengah | `100.000 – 1.000.000` |
| tinggi | `≥ 1.000.000` |

Distribusi kelas sengaja **imbalanced** (~60/30/10) melalui penyesuaian parameter marginal log-harga.

### 6.2 Agregat Gold

| Tabel | Dimensi | Metrik |
|-------|---------|--------|
| `tren_bulanan` | tahun, bulan | omzet, jumlah aktivitas, partisipan aktif, rata-rata |
| `omzet_kelas` | kelas_layanan | omzet total, share % |
| `omzet_geografis` | unit_geografis | omzet, transaksi, partisipan unik |
| `segmentasi_rfm` | id_partisipan | recency, frequency, monetary, segmen |

Agregat **tidak** di-copula; dihitung deterministik dari Silver sintesis.

### 6.3 Profil partisipan (modul wide-column store)

| Kolom | Sumber |
|-------|--------|
| `stats:omzet` | SUM(nilai_total) per partisipan |
| `stats:n_aktivitas` | COUNT per partisipan |
| `stats:tgl_terakhir` | MAX(tanggal) per partisipan |

---

## 7. Nilai enumerasi kanonik

Semua modul menggunakan set enum yang sama:

**Kelas layanan (6):**
`elektronik`, `fashion`, `makanan`, `kesehatan`, `otomotif`, `olahraga`

**Saluran interaksi (4):**
`mobile`, `web`, `atm`, `teller`

**Unit geografis (10):**
Jakarta, Surabaya, Bandung, Medan, Semarang, Makassar, Palembang, Denpasar, Yogyakarta, Balikpapan

**Tipe partisipan (4):**
`individu`, `organisasi_kecil`, `organisasi_menengah`, `platform`

**Segmen (3):**
`regular`, `loyal`, `prioritas`

**Status aktivitas (3):**
`sukses`, `pending`, `gagal`

**Lokasi sensor (5):**
`gudang-A`, `gudang-B`, `lantai-1`, `lantai-2`, `parkir`

---

## 8. Checklist validasi sebelum distribusi ke modul

- [ ] Matriks $\Sigma$ positif semi-definite setelah koreksi
- [ ] KS-test marginal: tidak ada kolom dengan $p < 0.01$ vs referensi (kecuali sengaja)
- [ ] Selisih korelasi Pearson ref vs synth $< 0.1$ untuk pasangan kunci
- [ ] 100% baris memenuhi constraint (non-negatif, enum valid, FK exist)
- [ ] `nilai_total` = produk komponen (deviasi floating $< 10^{-6}$)
- [ ] Seed 42 → hash checksum output identik antar run
- [ ] Anomali modul data quality hadir tepat 5 baris dengan tipe yang ditentukan
- [ ] Alias streaming ter-mapping tanpa kehilangan presisi nominal

---

## 9. Parameter volume per modul

| Modul | Partisipan | Aktivitas | Sensor events | Skor |
|-------|------------|-----------|---------------|------|
| Data lake intro | 50 | — | — | — |
| Spark intro | — | — | — | 10 |
| Medallion intro | 7 | 15 | — | — |
| Penyimpanan | 50 | 500 | — | — |
| Orkestrasi | — | 100 × hari simulasi | — | — |
| Streaming seed | — | 100 | 100 | — |
| ML | 200 | 10.000 | — | — |
| Viz / E2E | 300 | 15.000 | — | — |

Semua volume di-generate dari **satu pipeline copula** dengan parameter `n_rows`; bukan CSV terpisah yang dibuat manual.

---

## 10. Ringkasan

Penerapan Gaussian Copula pada dataset praktikum:

1. **Satu model entitas** — partisipan, aktivitas, unit layanan, sensor, skor — dengan relasi FK yang konsisten.
2. **Blok copula** — numerik log-transform, kategorik via pseudo-observasi, ordinal sebagai integer.
3. **Post-processing** — constraint, derived columns, anomali terkontrol, agregat Gold.
4. **Export modular** — volume dan alias berbeda per modul, schema kanonik tetap.

Hasilnya: peserta praktikum mengikuti **satu narasi data yang sama** dari modul pengenalan arsitektur hingga pipeline end-to-end, dengan hubungan statistik antarvariabel yang realistis dan reproducible.
