# Output — Studi Kasus Lingkungan

Empat artefak untuk audiens berbeda: BPBD kabupaten, KLHK/KPK, advokasi kesehatan, pelaporan iklim (NDC).

## Empat deliverable

| Folder | Output | Penerima | Frekuensi |
|---|---|---|---|
| [output-1-peta-risiko](output-1-peta-risiko/) | Peta risiko harian H3 + hotspot 24 jam | BPBD kab/kota | Harian 06:00 WIB |
| [output-2-akuntabilitas-konsesi](output-2-akuntabilitas-konsesi/) | Laporan akuntabilitas konsesi | KLHK, KPK | Bulanan |
| [output-3-dashboard-ispu-ispa](output-3-dashboard-ispu-ispa/) | Dashboard publik ISPU–ISPA | Masyarakat, advokasi | Mingguan |
| [output-4-emisi-karbon](output-4-emisi-karbon/) | Estimasi emisi CO₂e | NDC / UNFCCC | Per kejadian |

## Dokumentasi detail

→ **[PANDUAN-OUTPUT.md](output/PANDUAN-OUTPUT.md)**

## Alur Gold → output

```
gold.indeks_risiko_karhutla     → output-1 (PNG + GeoJSON + WhatsApp)
gold.hotspot_konsesi_agg        → output-2 (PDF + SIGAP)
gold.korelasi_ispu_ispa         → output-3 (Superset)
gold.emisi_karbon_konsesi       → output-4 (tabel + laporan kejadian)
```

## Menghasilkan artefak

```bash
cd ../arsitektur-lab && bash scripts/run_pipeline.sh
```

| Output | Status |
|---|---|
| 1–4 | ✅ `output/scripts/` |
