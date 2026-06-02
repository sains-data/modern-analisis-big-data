# Latihan 5 — Eksplorasi Mandiri
**Chapter 8 · Struktur & Penyimpanan Big Data** | Estimasi waktu: **25 menit**

## Tujuan

- Mendaftarkan external table ORC di Hive
- Mendesain row key HBase dengan reverse timestamp
- Menjawab pertanyaan diskusi arsitektur penyimpanan

## Prasyarat

- [ ] Latihan 1–4 selesai

## Bagian A — External Table ORC

```bash
cd sesi-praktikum/chapter-8/Konfigurasi-lab
bash scripts/run_silver_orc_hive.sh
```

Skrip: `app/silver_orc_hive.py` → `datalake.transaksi_orc`.

Bandingkan waktu query agregasi di Hive Shell pada `transaksi` (Parquet) vs `transaksi_orc` (ORC).

## Bagian B — HBase Row Key Reverse Timestamp

```bash
bash scripts/run_event_log_hbase.sh
```

Skrip: `app/event_log_hbase.py` — tabel `event_log`, scan harus menampilkan event terbaru pertama.

## Pertanyaan Diskusi

1. Mengapa pemilihan row key adalah keputusan paling kritis di HBase?
2. Berdasarkan benchmark, mengapa format kolumnar lebih efisien?
3. Dalam Medallion Iceberg, mengapa Bronze append-only sedangkan Silver memakai MERGE?
4. Kapan Gold memakai Hive Managed Table vs Iceberg?

## Penutup

```bash
bash scripts/verify_datalake.sh
bash stop.sh
```

---

*Latihan 5 selesai. Chapter 8 praktik tuntas.*
