# Panduan Arsitektur Lab — Analitik Stunting Sumatera Utara

Arsitektur **lima lapisan** dengan ritme **batch bulanan** (Posyandu) + **event-driven** (upload kader).

## Diagram logis

```
┌ INGEST ────────────────────────────────────────────────────────┐
│ e-PPGBM → Kafka │ Fasyankes API │ OSM+OSRM │ DTKS SFTP bulanan  │
└────────────┬───────────────────────────────┬───────────────────┘
             │ EVENT (upload balita)          │ BATCH (tgl 5/bulan)
             ▼                                ▼
     Spark Streaming                   Airflow + Sedona
     • validasi outlier                • ingest_eppgbm
     • alert BB ↓ >200g                • kalkulasi_zscore (LMS WHO)
     • → output.alert.kader            • agregasi_desa
                                       • join_aksesibilitas (OSRM)
                                       • indeks_risiko (5 dimensi)
             │                                │
             └────────────┬───────────────────┘
                          ▼
              LAKEHOUSE (Iceberg @ MinIO)
              prevalensi_stunting | skor_aksesibilitas
              indeks_risiko_multi | rekam_tumbuh (terenkripsi)
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
     DBSCAN          Moran's I      Regresi spasial
     XGBoost         KNN gap akses
                          ▼
   Prioritas 50 desa │ Dashboard TPPS │ Alert kader │ Bukti nakes
```

## Topik Kafka

| Topik | Arah | Isi |
|---|---|---|
| `balita.upload.sumut` | In | Event upload kader e-PPGBM |
| `output.alert.kader` | Out | Alert MERAH/ORANYE/KUNING |

**SLO alert:** &lt; **30 detik** dari upload ke notifikasi kader.

## DAG Airflow bulanan (tgl 5)

| Task | Fungsi |
|---|---|
| `ingest_eppgbm` | Tarik REST API terbaru |
| `kalkulasi_zscore` | TB/U, BB/U, BB/TB — formula LMS WHO |
| `agregasi_desa` | `prev_pct`, `n_stunting` per desa |
| `join_aksesibilitas` | Waktu tempuh desa → Puskesmas (OSRM) |
| `indeks_risiko` | 5 dimensi → `indeks_risiko_stunting_multifaktor` |

Jadwal: tanggal **5** (4 hari setelah batas upload kader tgl 1).

## Tabel Gold

| Tabel | Granularitas |
|---|---|
| `prevalensi_stunting` | Desa / bulan |
| `skor_aksesibilitas_fasyankes` | Desa — `waktu_tempuh_menit` |
| `indeks_risiko_stunting_multifaktor` | Desa / bulan — 5 skor dimensi |
| `rekam_tumbuh_kembang_balita` | Individu — **terenkripsi** |

## Lima dimensi indeks risiko (Product Owner Sprint 1)

Dokumentasikan bobot dan sumber per dimensi (contoh buku Output 1):

| Dimensi | Sumber tipikal |
|---|---|
| d1_prevalensi | e-PPGBM agregat desa |
| d2_sanitasi | STBM |
| d3_kemiskinan | DTKS / BPS |
| d4_akses_pusk | OSRM isokron |
| d5_air_bersih | STBM / BPS |

## OSRM / isokron

- Input: PBF OSM Sumatera Utara (~500 MB)  
- Build: `osrm-extract` + `osrm-partition` + `osrm-customize` (30–60 menit)  
- Ambang layanan minimal Kemkes: **&gt;60 menit** = aksesibilitas rendah  
- Zona output: **30 / 60 / 90 menit**

## Port layanan (rencana)

| Layanan | Port |
|---|---|
| Kafka | 9092 |
| Airflow | 8080 |
| OSRM | 5000 |
| MinIO | 9000/9001 |
| Superset (TPPS) | 8088 |

## Checklist Sprint 1

- [ ] Spike mapping kolom e-PPGBM  
- [ ] OSRM graph Sumut siap  
- [ ] Tabel `who_lms_standar` di Silver  
- [ ] Dokumen 5 dimensi + bobot disetujui  

## Checklist Sprint 2

- [ ] Consumer lag &lt; 5 event  
- [ ] Alert pipeline &lt; 30 detik  
- [ ] Prevalensi desa validasi 5 sampel manual  
- [ ] Tidak ada desa null waktu tempuh  

## Privasi

`rekam_tumbuh` berisi data individu balita — enkripsi at-rest, akses least privilege, jangan commit data produksi ke repo publik.

## Rujukan terkait

- [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md)  
- [../analitik/PANDUAN-ANALITIK.md](../analitik/PANDUAN-ANALITIK.md)  
- [../output/PANDUAN-OUTPUT.md](../output/PANDUAN-OUTPUT.md)  
