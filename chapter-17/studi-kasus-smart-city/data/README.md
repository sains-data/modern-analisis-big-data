# Data — Studi Kasus Smart City

Data transportasi, kualitas udara, dan sosial-ekonomi **Kota Medan**.

## Struktur

```
data/
├── README.md
├── KATALOG-DATA.md     # Tabel 17.17
├── sumber/
├── bronze/
├── silver/
└── gold/
```

## Medallion (ringkas)

| Layer | Contoh |
|---|---|
| **Bronze** | `jalan_medan`, `gtfs_tmd`, `openaq_raw`, `probe_stream` |
| **Silver** | `ruas_jalan`, `probe_mapped`, `pm25_grid`, `halte_tmd` |
| **Gold** | `lalu_lintas`, `kualitas_udara`, `korelasi_pm25`, `emisi` |

## Dokumentasi

→ **[KATALOG-DATA.md](KATALOG-DATA.md)**
