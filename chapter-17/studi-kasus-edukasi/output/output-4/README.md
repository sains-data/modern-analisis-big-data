# Output 4 — Dashboard Indikator Mutu BAN-PT

## Tujuan

Menghitung **indikator mutu akreditasi** secara otomatis dari lakehouse institusional dan mengekspornya ke format borang BAN-PT.

## Indikator (contoh)

| Indikator | Sumber agregat |
|---|---|
| Lulusan tepat waktu | SIA + aturan SKS |
| Rasio dosen : mahasiswa | SDM + SIA |
| IPK rata-rata program studi | `gold` agregat nilai |
| Kepuasan mahasiswa | Survei Silver |

## Artefak

| Artefak | Format |
|---|---|
| Dashboard Superset | Near-real-time terhadap Gold |
| Ekspor borang | Excel + PDF |

## Jadwal

**Per semester** (pembaruan otomatis saat Gold ter-refresh).

## Skrip referensi

`output_04_dashboard_banpt.py`.

## Impak kebijakan

Membebaskan tim akreditasi dari rekapitulasi manual; konsistensi angka lintas unit.
