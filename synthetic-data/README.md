# Sintesis Data Multivariat Berbasis Copula

Generator data sintesis **Gaussian Copula** untuk modul praktikum Bab 3–14.

## Isi folder

| Path | Ringkasan |
|------|-----------|
| [METODE-GAUSSIAN-COPULA.md](METODE-GAUSSIAN-COPULA.md) | Teori dan algoritma |
| [PENERAPAN-DATASET.md](PENERAPAN-DATASET.md) | Skema entitas dan pemetaan modul |
| [config/schema_v1.yaml](config/schema_v1.yaml) | Schema kanonik + parameter export |
| [generators/copula_gaussian.py](generators/copula_gaussian.py) | Generator Python |
| [scripts/generate.sh](scripts/generate.sh) | Generate semua output |
| [scripts/verify_outputs.sh](scripts/verify_outputs.sh) | Verifikasi volume & constraint |
| [scripts/sync_to_chapters.sh](scripts/sync_to_chapters.sh) | Deploy ke `chapter-*/Konfigurasi-lab/` |

## Quick start

```bash
cd synthetic-data

# 1. Generate (buat venv, install deps, tulis outputs/)
bash scripts/generate.sh

# 2. Verifikasi
bash scripts/verify_outputs.sh

# 3. Sync ke folder lab tiap bab
bash scripts/sync_to_chapters.sh
```

Generate modul tertentu saja:

```bash
bash scripts/generate.sh ch06_medallion
# atau
.venv/bin/python generators/copula_gaussian.py --module ch11_ml
```

Dry-run sync (tanpa menulis file):

```bash
DRY_RUN=1 bash scripts/sync_to_chapters.sh
```

## Output per modul

| Folder output | Bab | File utama |
|---------------|-----|------------|
| `ch03_minio` | 3 | `sample_users.csv` |
| `ch04_hadoop` | 4 | `latihan.txt`, `dataset_wordcount.txt` |
| `ch05_spark` | 5 | `mahasiswa.csv` |
| `ch06_medallion` | 6 | `transaksi.csv`, `pelanggan.csv` |
| `ch07_medallion_local` | 7 | salinan Bab 6 |
| `ch08_storage` | 8 | `transaksi.csv`, `pelanggan.csv` |
| `ch09_orchestration` | 9 | `transaksi_harian.csv`, `catatan_aktivitas_harian.csv` |
| `ch10_streaming` | 10 | `*.json` Kafka seed + kanonik |
| `ch11_ml` | 11 | `transaksi_ml.csv/json`, `pelanggan_agregat.json` |
| `ch12_viz` | 12 | `silver_transaksi.csv`, `gold_*.csv` (5 tabel) |
| `ch14_e2e` | 14 | `silver_transaksi.csv`, `gold_*.csv` (5 tabel, sama volume Bab 12) |

## Dependensi

```
numpy>=1.24
pyyaml>=6.0
scipy>=1.10
```

Virtualenv lokal (`.venv/`) dibuat otomatis oleh `scripts/generate.sh`.

## Alur kerja

```
schema_v1.yaml
      │
      ▼
copula_gaussian.py  ──►  outputs/{modul}/
      │
      ├── verify_outputs.sh
      └── sync_to_chapters.sh  ──►  chapter-*/Konfigurasi-lab/data/
```

Seed default: `42` (reproduksibel). Override: `--seed 123`.
