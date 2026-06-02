# Katalog Data — Big Data Perguruan Tinggi

Merujuk **Tabel data institusional** (`tab:17-data-pt`, `chapter-17.tex`).

## Katalog

| Dataset | Sumber | Format | Pembaruan | Folder `sumber/` |
|---|---|---|---|---|
| Rekam nilai / transkrip | SIA internal | PostgreSQL/CSV | Per semester | `sia/nilai/` |
| Log aktivitas LMS | Moodle/Canvas | JSON/CSV | Real-time | `lms/events/` |
| Absensi kuliah | Sistem absensi | CSV/stream | Per sesi | `absensi/` |
| Data keuangan mahasiswa | Keuangan internal | CSV | Bulanan | `keuangan/` |
| Lowongan kerja | LinkedIn + Jobstreet API | JSON | Harian | `karir/lowongan/` |
| Data akreditasi | [BAN-PT](https://ban-pt.kemdikbud.go.id) | Excel/CSV | Tahunan | `akreditasi/banpt/` |
| Jadwal & ruang | Penjadwalan internal | iCal/CSV | Per semester | `akademik/jadwal/` |
| Survei kepuasan | LimeSurvey / Forms | CSV | Per semester | `survei/` |
| Tracer study | [Dikti Tracer](https://tracerstudy.kemdikbud.go.id) | Excel/API | Tahunan | `tracer/` |

## Pemetaan ke `mahasiswa_id`

Semua sumber yang memuat NIM harus melalui:

```
mahasiswa_id = SHA256(salt_institusi || NIM)
```

**Tidak ada** kolom NIM asli di Bronze/Gold yang di-commit ke repo.

## Skema medallion

### Bronze

| Tabel | Catatan |
|---|---|
| `bronze.sia` | Nilai, status akademik |
| `bronze.lms_events` | Event log mentah |
| `bronze.absensi_sesi` | Per pertemuan |
| `bronze.lowongan_kerja` | Teks deskripsi pekerjaan |
| `bronze.kurikulum` | CPL per mata kuliah |

### Silver

| Tabel | Transformasi |
|---|---|
| `silver.lms_events` | Parsed, semester, event_type |
| `silver.nilai_akademik` | IPK, tren semester |
| `silver.absensi` | `persen_hadir` per MK |
| `silver.bimbingan_akademik` | `mahasiswa_id` ↔ `dosen_pa_id` |

### Gold

| Tabel | Deskripsi |
|---|---|
| `gold.dataset_model_risiko` | 47 fitur + label |
| `gold.profil_risiko_mahasiswa` | Skor mingguan |
| `gold.kinerja_matkul` | Agregat bottleneck |
| `gold.utilisasi_ruang` | Slot × ruang |
| `gold.skill_gap_kurikulum` | Kata/skill vs CPL |
| `gold.indikator_banpt` | Indikator akreditasi otomatis |

## 47 fitur (empat dimensi — ringkas)

| Dimensi | Contoh fitur (buku) |
|---|---|
| Keterlibatan LMS | f1–f8: events, hari aktif, tugas, diskusi, pola deadline |
| Performa akademik | f9–f13: IPK, nilai D/E, tren |
| Kehadiran | f14–f17: % hadir, absen total |
| Keuangan | (fitur tambahan di pipeline lengkap) |

## Konvensi

```
sumber/lms/events_YYYYMMDD.parquet
gold/profil_risiko_mahasiswa/minggu=YYYY-Www/
```

## Pengganti offline

| Produksi | Lab |
|---|---|
| SIA penuh | CSV 3.000 mahasiswa sintetis |
| LMS logs | Generator event Moodle-like |
| Lowongan | 500 postingan TI/data science |

## Gate Silver

1. `mahasiswa_id` joinable lintas SIA, LMS, absensi.  
2. Semester (`2024-1`) konsisten.  
3. Missing rate per fitur ≤30% sebelum training.  
