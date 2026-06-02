# Analitik — Studi Kasus Konservasi

NDVI multitemporal, KDE home range, streaming alert GPS, Gi* konflik, coverage gap patroli.

## Isi yang direncanakan (Lampiran)

```
analitik/
├── batch/           # deforestasi, KDE, coverage_gap
├── streaming/       # alert konflik, chainsaw forward
├── edge/            # inferensi YOLO/CNN (referensi)
├── model/           # Random Forest prediksi deforestasi
└── notebooks/       # Visualisasi trajektori, Gi*
```

## Dokumentasi

→ **[PANDUAN-ANALITIK.md](analitik/PANDUAN-ANALITIK.md)**

## Metrik

| Analitik | Target |
|---|---|
| Alert gajah → desa | &lt; 5 menit |
| Lag streaming simulasi | &lt; 3 menit |
| KDE overlap konsesi | Terhitung per individu |
