# Output — Studi Kasus Kesehatan

Empat artefak untuk kader, TPPS, Dinkes/Bappeda, dan kebijakan pusat.

## Empat deliverable

| Folder | Output | Penerima | Frekuensi |
|---|---|---|---|
| [output-1-prioritas-desa](output-1-prioritas-desa/) | 50 desa terburuk per kabupaten | Dana Desa, Dinkes | Bulanan |
| [output-2-dashboard-tpps](output-2-dashboard-tpps/) | Dashboard TPPS Provinsi | TPPS Sumut | Mingguan |
| [output-3-alert-kader](output-3-alert-kader/) | Alert Posyandu real-time | Kader desa | Real-time |
| [output-4-bukti-nakes](output-4-bukti-nakes/) | Basis bukti tenaga kesehatan | Bappeda, Kemenkes | Triwulanan |

## Dokumentasi

→ **[PANDUAN-OUTPUT.md](output/PANDUAN-OUTPUT.md)**

## Alur Gold → output

```
gold.indeks_risiko_stunting_multifaktor  → output-1
gold.prevalensi_stunting + aksesibilitas → output-2 (Superset)
streaming alert                          → output-3
gold.skor_aksesibilitas + kapasitas Puskesmas → output-4
```

## Menghasilkan artefak

```bash
cd ../arsitektur-lab && bash scripts/run_pipeline.sh
```

| Output | Status |
|---|---|
| 1–4 | ✅ skrip di `output/scripts/` |
