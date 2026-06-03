# Latihan 5 — SQL Lab & Eksplorasi Mandiri
**Chapter 12 · Visualisasi dan Eksplorasi Data** | Estimasi: **30 menit** | **Tahap 5** (Bab 12)

## Tujuan

- Menjalankan query analitik di **SQL Lab** (§12-4-4)
- **Tugas A:** analisis MoM growth
- **Tugas B:** Donut Chart vs Treemap komposisi kategori
- Menjawab pertanyaan refleksi buku

## Prasyarat

- [ ] Latihan 1–4 selesai
- [ ] Database `Analitik E-Commerce` terhubung
- [ ] Kolom `mom_growth_pct`, `ma3_omzet` di `tren_bulanan` — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Langkah 5.1 — Query dari buku

**SQL → SQL Lab** — database `Analitik E-Commerce`, schema `public`.

**Analisis 1 — Omzet per kota (top 15):**

```sql
SELECT
    kota,
    SUM(omzet)       AS total_omzet,
    SUM(transaksi)   AS total_transaksi,
    ROUND(SUM(omzet)::numeric /
          NULLIF(SUM(transaksi), 0), 0) AS avg_nilai_per_trx,
    SUM(pelanggan_unik)                 AS total_pelanggan
FROM omzet_kota
GROUP BY kota
ORDER BY total_omzet DESC
LIMIT 15;
```

**Analisis 2 — Status pertumbuhan bulanan:**

```sql
SELECT
    periode,
    omzet,
    ma3_omzet,
    mom_growth_pct,
    CASE
        WHEN mom_growth_pct > 10 THEN 'Pertumbuhan Tinggi'
        WHEN mom_growth_pct < 0  THEN 'Kontraksi'
        ELSE 'Pertumbuhan Normal'
    END AS status_pertumbuhan
FROM tren_bulanan
ORDER BY mom_growth_pct DESC;
```

**Analisis 3 — Kategori nilai transaksi tertinggi:**

```sql
SELECT
    kategori,
    omzet_total,
    jumlah_transaksi,
    ROUND(omzet_rata, 0)     AS avg_nilai,
    persen_omzet             AS kontribusi_pct
FROM omzet_kategori
WHERE jumlah_transaksi >= 50
ORDER BY omzet_rata DESC;
```

## Tugas A — Growth Rate Analysis

Tulis query untuk:

1. Tiga bulan dengan `mom_growth_pct` tertinggi dan terendah
2. Bulan dengan `omzet` di bawah `ma3_omzet`

Buat **chart** dari hasil (pilih tipe yang tepat di Explore).

## Tugas B — Komposisi Omzet

Dari dataset `omzet_kategori`:

1. Buat **Donut Chart** — metric `SUM(omzet_total)`, dimension `kategori`
2. Buat **Treemap** — data yang sama
3. Bandingkan keterbacaan — mana lebih mudah dibaca dan mengapa?

## Pertanyaan refleksi (buku)

1. Superset tidak menyimpan data — hanya query ke PostgreSQL setiap render. Keuntungan dan keterbatasan?
2. Mengapa MA3 lebih berguna daripada omzet aktual saja?
3. Mengapa bulan November cenderung omzet tertinggi pada dataset latihan?
4. Kapan memakai **Explore** vs **SQL Lab**?

## Penutup

```bash
cd sesi-praktikum/chapter-12/Konfigurasi-lab
bash stop-viz.sh
bash stop-spark.sh
```

---

*Latihan 5 selesai. Chapter 12 praktik tuntas.*
