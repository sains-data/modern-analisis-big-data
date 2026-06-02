# Latihan 5 — Validasi End-to-End dan Latihan Lanjutan
**Chapter 3 · Desain Arsitektur dan Platform Big Data** | Estimasi waktu: **20 menit**

## Tujuan

- Memvalidasi alur penuh `Bronze -> Silver -> Gold`
- Mengulang pola yang sama untuk dataset lain

## Prasyarat

- [ ] Latihan 1–4 selesai
- [ ] Object tersedia di ketiga bucket

## Bagian A — Verifikasi End-to-End

```bash
cd ../Konfigurasi-lab
docker exec -it bigdata-compute python verify_pipeline.py
```

Atau lewat `mc`:

```bash
docker exec -it bigdata-mc bash -c "
  echo '=== BRONZE ===' && mc ls local/bronze --recursive
  echo '=== SILVER ===' && mc ls local/silver --recursive
  echo '=== GOLD   ===' && mc ls local/gold --recursive
"
```

Pastikan minimum ada:
- `bronze/users/sample_users.csv`
- `silver/users/users_clean.parquet`
- `gold/summary/city_summary.parquet`

## Bagian B — Latihan Lanjutan (World Happiness Report)

Gunakan dataset:
`https://ourworldindata.org/happiness-and-life-satisfaction`

Tugas:
1. Upload CSV ke Bronze (`bronze/happiness_raw.csv`)
2. Transform ke Silver:
   - hapus baris null
   - standarisasi nama kolom
   - tambah `processed_at`
   - simpan Parquet
3. Agregasi ke Gold:
   - rata-rata `life_ladder` per negara
   - rata-rata `gdp_per_capita` per negara
   - simpan `gold/country_summary.parquet`
4. Tampilkan 5 negara dengan skor kebahagiaan tertinggi

## Refleksi

- Apa manfaat utama bucket Bronze yang immutable?
- Kenapa format Parquet dipakai di Silver/Gold, bukan CSV?
- Bagaimana `data lineage` membantu debugging pipeline?

---

*Latihan 5 selesai. Chapter 3 praktik tuntas.*
