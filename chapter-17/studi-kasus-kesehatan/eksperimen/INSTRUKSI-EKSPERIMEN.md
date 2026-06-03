# Instruksi Eksperimen — Analitik Stunting Sumatera Utara

## Langkah 0 — Persiapan

```bash
cd sesi-praktikum/chapter-17/studi-kasus-kesehatan/eksperimen/catatan
cp template-log-eksperimen.md log-eksperimen-$(date +%Y%m%d).md
```

Baca [CHECKLIST-SPRINT.md](CHECKLIST-SPRINT.md).

---

## Langkah 1 — Folder eksekusi

```bash
cd ../arsitektur-lab
chmod +x *.sh scripts/*.sh
cp .env.example .env   # opsional
```

---

## Langkah 2 — Data sintetis (Sprint 1)

```bash
bash scripts/prepare_data.sh
```

**Verifikasi:**

```bash
ls ../data/sumber/eppgbm/eppgbm_202605.csv
ls ../data/sumber/batas/desa_sumut.geojson
ls ../data/sumber/who/who_lms_tb_u.csv
```

**Validasi manual z-score:** pilih 10 balita, hitung z TB/U dengan rumus LMS (lihat [../data/KATALOG-DATA.md](../data/KATALOG-DATA.md)).

---

## Langkah 3 — Pipeline (Sprint 2)

```bash
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
```

| Tahap | Skrip | Output Gold |
|---|---|---|
| Ingest | `ingest_static.py` | Silver WHO, desa, STBM |
| Z-score | `kalkulasi_zscore.py` | `data_balita`, `rekam_tumbuh_balita` |
| Prevalensi | `agregasi_prevalensi.py` | `prevalensi_stunting` |
| Akses | `aksesibilitas_puskesmas.py` | `skor_aksesibilitas` |
| Indeks | `indeks_risiko.py` | `indeks_risiko`, `prioritas_desa_bulanan` |
| Spasial | `spatial_analytics.py` | `klaster_spasial` (DBSCAN, Moran's I) |
| Alert | `alert_kader_stream.py` | `alert_kader` |

---

## Langkah 4 — Verifikasi

```bash
bash scripts/verify_stack.sh
```

Target: prevalensi provinsi ~20–25% (sintetis), tidak ada desa null `waktu_tempuh_menit`.

---

## Langkah 5 — Output 1–4 (Sprint 3)

| Output | Folder | File kunci |
|---|---|---|
| 1 Prioritas desa | `output/output-1-prioritas-desa/` | `prioritas_desa_latest.csv`, `.geojson` |
| 2 Dashboard TPPS | `output/output-2-dashboard-tpps/` | `tren_provinsi.json`, `stunting_kab_bulan_ini.geojson` |
| 3 Alert kader | `output/output-3-alert-kader/` | `alert_log_latest.jsonl` |
| 4 Bukti nakes | `output/output-4-bukti-nakes/` | `laporan_nakes_ringkasan.pdf` |

**Demo TPPS:** buka GeoJSON kabupaten di Kepler.gl; bandingkan `prev_pct_provinsi` vs target 14%.

---

## Langkah 6 — Kafka (opsional)

```bash
docker compose up -d
bash scripts/init_kafka.sh
python ../analitik/streaming/alert_kader_stream.py --source kafka
```

Topik: `balita.upload.sumut` → `output.alert.kader`.

---

## Langkah 7 — Eksperimen lanjutan

- Ubah bobot di `analitik/lib/config.py` → ulangi `indeks_risiko.py`  
- Uji alert MERAH: edit `upload_events.jsonl` (ΔBB &lt; −200 g)  
- Bandingkan haversine lab vs OSRM produksi (dokumentasi di laporan)

---

## Langkah 8 — Pengumpulan

- Log + bukti di `eksperimen/catatan/`  
- [retrospective-sprint3.md](catatan/retrospective-sprint3.md)  
- Diskusi privasi: `rekam_tumbuh_balita` tidak boleh di-commit ke repo publik

**Reset:** `bash reset.sh` dari `arsitektur-lab/`.
