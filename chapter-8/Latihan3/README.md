# Latihan 3 — Eksplorasi HBase
**Chapter 8 · Struktur & Penyimpanan Big Data** | Estimasi waktu: **35 menit**

## Tujuan

- Agregasi profil pelanggan dari Silver dengan Spark
- Menulis hasil ke HBase via `happybase` (batch put)
- Memverifikasi data di tabel `profil_pelanggan`

## Prasyarat

- [ ] Latihan 2 selesai — Silver Parquet tersedia
- [ ] HBase Thrift aktif (port `9090` di dalam kontainer)

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Input | `hdfs:///datalake/silver/transaksi/` |
| Tabel HBase | `profil_pelanggan` |
| Script | `Konfigurasi-lab/app/spark_ke_hbase.py` |
| HBase UI | http://localhost:16010 |

## Langkah Kerja

### 1) Pastikan layanan HBase

```bash
cd sesi-praktikum/chapter-8/Konfigurasi-lab
bash scripts/setup_services.sh
```

### 2) Jalankan Spark → HBase

```bash
bash scripts/run_spark_ke_hbase.sh
```

### 3) Verifikasi HBase Shell (opsional)

```bash
bash login.sh
hbase shell
```

```
scan 'profil_pelanggan', {LIMIT => 3}
get 'profil_pelanggan', 'PLG-0001'
```

## Hasil yang Dicatat

- Jumlah profil yang ditulis
- Contoh 3 baris dari `scan`
- Perbandingan use case: kapan Hive vs HBase?

## Refleksi Singkat

1. Mengapa row key = `id_pelanggan` masuk akal untuk profil agregat?
2. Apa risiko hot-spot jika row key selalu monoton naik?

---

*Latihan 3 selesai. Lanjut ke **Latihan 4 — Benchmark Format**.*
