# Laporan After-Action — Simulasi Banjir DAS Musi

**Dibuat:** 2026-06-03T03:28:34.130933+00:00

## 1. Ringkasan kejadian

- Stasiun referensi **KAYU_AGUNG** mencapai TMA puncak **1043.8 cm**
  pada window `2026-05-27 11:45:00+00:00` dengan level **MERAH**.
- Deret observasi: 48 window 15 menit dalam simulasi lab.

## 2. Kinerja sistem (SLO)

| Metrik | Target | Catatan lab |
|---|---|---|
| Sensor → peta terdampak | ≤ 5 menit | Pipeline batch/file; ukur di demo Sprint 3 |
| Spatial join | < 60 detik | Python/geopandas pada 50 kelurahan |
| False alarm | Minim | Validasi manual BBWS jika data produksi |

## 3. Dampak estimasi

- **63,517** jiwa estimasi terdampak di **22** kelurahan.
- **3** shelter digunakan dalam rencana routing.
- Metode: proporsi luas genangan ∩ kelurahan × populasi BPS (asumsi kepadatan merata).

## 4. Lessons learned (Scrum)

- Sprint 1: anonimisasi tidak diperlukan; fokus kualitas geometri dan CRS.
- Sprint 2: selaraskan ambang TMA dengan SOP BPBD setempat.
- Sprint 3: uji end-to-end dengan skenario MERAH terdokumentasi.

## 5. Rekomendasi

- Tambah sensor hulu DAS; pertimbangkan WorldPop 100 m untuk estimasi populasi.
- Produksi: ganti KNN Euclidean dengan routing jalan + constraint genangan (Sedona).
- Deploy PySpark streaming + Iceberg pada cluster yang sama dengan Bab 16.
