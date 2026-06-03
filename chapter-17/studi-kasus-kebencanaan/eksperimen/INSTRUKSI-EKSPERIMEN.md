# Instruksi Eksperimen — Peringatan Dini Banjir DAS Musi

Panduan langkah demi langkah untuk praktikum. Ikuti **berurutan** kecuali langkah yang ditandai opsional.

---

## Ringkasan alur

```mermaid
flowchart LR
  A[Langkah 0–1 Setup] --> B[Langkah 2 Data sintetis]
  B --> C[Langkah 3 Pipeline]
  C --> D[Langkah 4 Verifikasi Gold]
  D --> E[Langkah 5 Output 1–4]
  E --> F[Langkah 6 Kafka opsional]
  F --> G[Langkah 7–8 Catatan & demo]
```

---

## Langkah 0 — Persiapan lingkungan

**Lokasi terminal:** belum menjalankan kode; baca dulu.

1. Clone/buka repositori `penelitian-bigdata`.  
2. Pastikan path studi kasus ada:
   ```text
   sesi-praktikum/chapter-17/studi-kasus-kebencanaan/
   ```
3. Buat salinan log eksperimen:
   ```bash
   cd sesi-praktikum/chapter-17/studi-kasus-kebencanaan/eksperimen/catatan
   cp template-log-eksperimen.md log-eksperimen-$(date +%Y%m%d).md
   ```
4. Centang **Prasyarat** di [CHECKLIST-SPRINT.md](CHECKLIST-SPRINT.md).

---

## Langkah 1 — Masuk ke folder eksekusi

**Ini folder utama untuk semua perintah `bash` dan `python` pipeline.**

```bash
cd sesi-praktikum/chapter-17/studi-kasus-kebencanaan/arsitektur-lab
chmod +x *.sh scripts/*.sh
```

Opsional — salin environment:

```bash
cp .env.example .env
```

**Catat di log:** folder kerja = `arsitektur-lab`, waktu mulai.

---

## Langkah 2 — Generate data sintetis (Sprint 1)

**Perintah** (dari `arsitektur-lab/`):

```bash
bash scripts/prepare_data.sh
```

**Yang terjadi:**
- Skrip di `../data/scripts/` membuat kelurahan, genangan, shelter, sensor TMA, hujan BMKG.  
- Output awal di `../data/sumber/`.

**Verifikasi:**

```bash
ls ../data/sumber/kelurahan_sumsel.geojson
ls ../data/sumber/sensor/tma_musi/tma_readings.jsonl
```

**Harus Anda lakukan di `eksperimen/`:**
- Centang Sprint 1 bagian *data sintetis* di [CHECKLIST-SPRINT.md](CHECKLIST-SPRINT.md).  
- Catat jumlah kelurahan (50) dan stasiun (10) di log.

**Jika gagal:** `pip` akan membuat `.venv` di `arsitektur-lab/` — tunggu hingga selesai, lalu ulangi perintah.

---

## Langkah 3 — Jalankan pipeline analitik (Sprint 2)

**Perintah** (masih di `arsitektur-lab/`):

```bash
export PYTHONPATH="$(cd .. && pwd)"
bash scripts/run_pipeline.sh
```

**Yang dijalankan (otomatis, berurutan):**

| Urutan | Skrip | Hasil |
|---|---|---|
| 1 | `analitik/batch/ingest_static.py` | Bronze + Silver Parquet |
| 2 | `analitik/batch/aggregate_tma.py` | `data/gold/tma_latest.parquet` |
| 3 | `analitik/streaming/tma_siaga_stream.py` | `data/gold/tma_siaga_hourly.parquet` |
| 4 | `analitik/batch/populasi_terdampak.py` | `data/gold/populasi_terdampak.parquet` |
| 5 | `analitik/batch/routing_evakuasi.py` | `data/gold/rute_evakuasi.parquet` |
| 6–9 | `output/scripts/output_01` … `output_04` | Folder `../output/output-*` |

**Perhatikan stdout:** baris `[REF] KAYU_AGUNG` dan `[OK] estimasi total terdampak`.

**Harus Anda lakukan:**
- Salin 3–5 baris output penting ke `eksperimen/catatan/log-eksperimen-*.md`.  
- Centang Sprint 2 di checklist.

---

## Langkah 4 — Verifikasi artefak Gold

```bash
bash scripts/verify_stack.sh
```

Semua baris harus `[OK]`. Jika `[MISS]`:

| File hilang | Tindakan |
|---|---|
| `populasi_terdampak.parquet` | Pastikan siaga KAYU_AGUNG ≥ ORANYE; ulangi Langkah 2–3 |
| `rute_evakuasi.parquet` | Bergantung populasi; perbaiki dulu join spasial |
| PDF logistik | Jalankan `python ../output/scripts/output_03_logistik.py` |

**Eksplorasi manual (opsional):**

```bash
export PYTHONPATH="$(cd .. && pwd)"
python -c "
import pandas as pd
from pathlib import Path
g = Path('..')/'data'/'gold'
print(pd.read_parquet(g/'tma_latest.parquet').head())
print('terdampak:', pd.read_parquet(g/'populasi_terdampak.parquet')['estimasi_terdampak'].sum())
"
```

---

## Langkah 5 — Periksa empat output (Sprint 3)

**Lokasi artefak** (relatif dari `studi-kasus-kebencanaan/`):

| Output | Path | File kunci |
|---|---|---|
| 1 Siaga | `output/output-1-level-siaga/` | `alert_latest.json`, `notifikasi_template.txt` |
| 2 Peta | `output/output-2-peta-terdampak/` | `terdampak_latest.geojson`, `kepler_config.json` |
| 3 Logistik | `output/output-3-logistik/` | `logistik_ringkasan.pdf` |
| 4 Evaluasi | `output/output-4-after-action/` | `after_action_latest.md` |

**Tugas Anda:**

1. Buka `alert_latest.json` — pastikan `"siaga": "MERAH"` atau `"ORANYE"` pada skenario uji.  
2. Buka `notifikasi_template.txt` — baca sebagai operator BPBD (bahasa Indonesia).  
3. Import `terdampak_latest.geojson` ke [Kepler.gl](https://kepler.gl) (drag & drop) + bandingkan dengan `kepler_config.json`.  
4. Buka PDF logistik — cek kapasitas vs estimasi pengungsi.  
5. Baca `after_action_latest.md` — lengkapi bagian *Lessons learned* di salinan Anda.

**Harus di `eksperimen/catatan/`:**
- Buat folder `bukti/` dan simpan 1 screenshot peta + 1 cuplikan JSON siaga.  
- Centang Sprint 3 di checklist.

---

## Langkah 6 — Mode Kafka (opsional, jika Docker tersedia)

**Dari `arsitektur-lab/`:**

```bash
docker compose up -d
sleep 25
bash scripts/init_kafka.sh
export PYTHONPATH="$(cd .. && pwd)"
python ../analitik/streaming/tma_siaga_stream.py --source kafka
```

**Tujuan eksperimen:** membandingkan pipeline *file* vs *streaming* Kafka (Bab 9).

**Catat di log:** apakah consumer menerima ≥ 80 event; lag (perkiraan) dari waktu publish.

```bash
docker compose down   # setelah selesai
```

Atau gunakan satu perintah: `bash start.sh` (setup + pipeline + Kafka publish).

---

## Langkah 7 — Eksperimen lanjutan (opsional)

Pilih **minimal satu** untuk laporan:

| Eksperimen | Cara | Pertanyaan yang diuji |
|---|---|---|
| Ubah ambang siaga | Edit `analitik/lib/config.py` → ulangi Langkah 3 | Sensitivitas peringatan |
| Tanpa hujan BMKG | Kosongkan kolom hujan di CSV sumber → regenerate | Peran curah hujan vs TMA |
| Satu genangan | Edit `data/scripts/generate_spatial_layers.py` | Perubahan estimasi populasi |
| SQL referensi | Baca `analitik/sql/populasi_terdampak.sql` | Persiapan porting ke Sedona |

Dokumentasikan hipotesis, perubahan, dan hasil di log eksperimen.

---

## Langkah 8 — Penutupan & retrospective

1. Isi [catatan/retrospective-sprint3.md](catatan/retrospective-sprint3.md) (template disediakan).  
2. Pastikan [CHECKLIST-SPRINT.md](CHECKLIST-SPRINT.md) tercentang penuh.  
3. Kumpulkan ke dosen/asisten:
   - `eksperimen/catatan/log-eksperimen-*.md`
   - `eksperimen/catatan/bukti/` (screenshot)
   - `eksperimen/catatan/retrospective-sprint3.md`
   - Opsional: zip folder `output/` sebagai bukti artefak.

**Reset lab** (hanya jika perlu ulang dari nol):

```bash
cd arsitektur-lab && bash reset.sh
```

---

## Troubleshooting

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| `ImportError: pyarrow` | Dependensi belum terpasang | `arsitektur-lab/.venv/bin/pip install -r requirements.txt` |
| `ModuleNotFoundError: analitik` | PYTHONPATH salah | `export PYTHONPATH="$(cd .. && pwd)"` dari `arsitektur-lab` |
| Populasi terdampak kosong | Siaga belum ORANYE/MERAH | Ulangi `prepare_data.sh`; cek `tma_latest` |
| Kafka connection refused | Docker belum up | `docker compose up -d` atau lewati Langkah 6 |
| Port 9093/9030 bentrok | Bab lain pakai port sama | Edit `docker-compose.yml` atau hentikan container lain |

---

## Pemetaan folder ↔ sprint Scrum

| Sprint | Langkah instruksi | Folder yang terisi |
|---|---|---|
| 1 | 0–2 | `data/sumber/`, `data/bronze/`, `data/silver/` |
| 2 | 3–4 | `data/gold/`, `analitik/` (eksekusi) |
| 3 | 5–8 | `output/`, `eksperimen/catatan/` |

---

## Rujukan

- [../arsitektur-lab/README.md](../arsitektur-lab/README.md) — ringkasan stack  
- [../analitik/PANDUAN-ANALITIK.md](../analitik/PANDUAN-ANALITIK.md) — detail analitik  
- [../output/PANDUAN-OUTPUT.md](../output/PANDUAN-OUTPUT.md) — SLO & format deliverable
