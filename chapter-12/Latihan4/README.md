# Latihan 4 — Dashboard Interaktif
**Chapter 12 · Visualisasi dan Eksplorasi Data** | Estimasi: **25 menit** | **Tahap 4** (Bab 12)

## Tujuan

- Membangun dashboard **`Analitik E-Commerce 2024`**
- Menyusun layout sesuai Gambar 12 (buku)
- Mengonfigurasi **Native Filter** dan menguji interaktivitas

## Prasyarat

- [ ] Latihan 3 — keempat chart tersimpan

## Layout (sesuai buku §12-prak-4)

```
┌────────────────────────────────────────────┐
│  Header: Ringkasan Bisnis 2024           │
│  Total Omzet (Big Number) — lebar penuh  │
├──────────────────────┬─────────────────────┤
│ Tren Omzet + MA3     │ Omzet per Kategori  │
│ (Line)               │ (Bar)               │
├──────────────────────┴─────────────────────┤
│ Ranking Kota (Table) — lebar penuh       │
└────────────────────────────────────────────┘
```

## Langkah kerja

### 4.1 Buat dashboard

1. **Dashboards → + Dashboard** → nama: `Analitik E-Commerce 2024`
2. **Edit Dashboard** — seret chart dari panel kiri
3. Tambahkan **Header** teks `Ringkasan Bisnis 2024` di atas Big Number
4. **Save**

### 4.2 Native Filter (§12-5-3)

**Filters → + Add/Edit Filters**

| Filter | Tipe | Default | Scoping |
|---|---|---|---|
| Periode Analisis | Time Range | Last 3 months | Chart dengan kolom temporal |
| Kategori Produk | Value (`kategori`) | — | Bar kategori, Line tren |
| Kota | Value (`kota`) | — | Table kota |

### 4.3 Uji interaktivitas

- Ubah **Periode** ke *Last 6 months* — apakah Line & Big Number berubah?
- Filter satu **kategori** — chart mana yang merespons?
- **Present Mode** (ikon layar penuh)

## Catatan

| Uji | Hasil |
|---|---|
| Filter periode mengubah Line Chart | Ya / Tidak |
| Filter kategori | Chart yang berubah: |
| Present Mode | |

## Refleksi

1. Mengapa Big Number ditempatkan paling atas (hierarki informasi)?
2. Filter `Kategori` tidak memfilter `Ranking Kota` jika tabel kota tidak punya kolom `kategori` — bagaimana solusinya di produksi?

---

*Latihan 4 selesai. Lanjut **Latihan 5 — SQL Lab (Tahap 5)**.*
