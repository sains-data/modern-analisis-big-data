# Output 2 — Optimasi Penjadwalan & Utilisasi Ruang

## Tujuan

Mengidentifikasi slot ruang **TIDAK EFISIEN** dan pasangan mata kuliah kecil yang dapat **dikonsolidasi** sebelum penjadwalan semester berikutnya.

## Metrik

| Status | `utilisasi_pct` |
|---|---|
| OPTIMAL | ≥ 80% |
| CUKUP | ≥ 50% |
| RENDAH | ≥ 30% |
| TIDAK EFISIEN | &lt; 30% |

## Sumber data

`silver.jadwal_kuliah` + `silver.absensi` → `gold.utilisasi_ruang`.

## Artefak

- Tabel utilisasi per `ruang_id` × `hari` × `slot_waktu`  
- Daftar pasangan MK untuk konsolidasi (&lt;20 mahasiswa, slot sama)

## Jadwal

**Per semester** — setelah UAS, sebelum scheduling baru.

## Skrip referensi

`output_02_utilisasi_ruang.py`.

## Impak kebijakan

Efisiensi sarana prasarana; mengurangi kelas paralel under-enrolled.
