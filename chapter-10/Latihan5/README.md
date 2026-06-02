# Latihan 5 — Eksplorasi: Windowing dan Delivery Semantics
**Chapter 10 · Analitik Aliran Data** | Estimasi waktu: **10 menit**

---

## Tujuan Latihan

Setelah menyelesaikan latihan ini, mahasiswa mampu:
- Membandingkan perilaku tumbling window dan sliding window secara eksperimental
- Menjelaskan mengapa sliding window menghasilkan lebih banyak baris output
- Menganalisis delivery semantics melalui eksperimen consumer dengan commit manual
- Menghubungkan temuan eksperimen dengan teori at-least-once semantics
- Menjawab pertanyaan diskusi konseptual tentang desain sistem streaming

---

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Python 3.10 atau 3.11 (bukan 3.12)
- [ ] Latihan 1–4 sudah selesai
- [ ] Stack Kafka masih berjalan
- [ ] Virtual environment aktif (`source ../Konfigurasi-lab/.venv/bin/activate`)
- [ ] Producer Python aktif (atau bisa dijalankan ulang)

---

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Folder kerja | `Konfigurasi-lab/` |
| Script window | `spark/window_comparison.py` |
| Script consumer | `scripts/consumer_semantics.py` |
| Spark UI | http://localhost:4040 |

> Semua perintah di latihan ini dijalankan dari folder **`Konfigurasi-lab/`** dengan venv aktif.

---

## Bagian A — Sliding Window vs. Tumbling Window

### Langkah A.1 — Hentikan pipeline lama (jika masih berjalan)

Di terminal Spark, tekan `Ctrl+C`. Kita akan menjalankan script baru.

Hapus checkpoint lama agar tidak konflik:

```bash
rm -rf /tmp/checkpoints/exp_a/
```

---

### Langkah A.2 — Pastikan producer aktif

```bash
cd ../Konfigurasi-lab
source .venv/bin/activate
python scripts/producer_transaksi.py
```

Biarkan berjalan di Terminal 1.

---

### Langkah A.3 — Tinjau script perbandingan window

Buka dan baca `Konfigurasi-lab/spark/window_comparison.py`. Script ini menjalankan dua query paralel:
- **Tumbling window:** lebar 2 menit, tidak overlap
- **Sliding window:** lebar 2 menit, slide setiap 1 menit

---

### Langkah A.4 — Jalankan script

Di Terminal 2:

```bash
cd ../Konfigurasi-lab
source .venv/bin/activate
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 \
  --master local[2] \
  --conf spark.sql.shuffle.partitions=4 \
  spark/window_comparison.py
```

Tunggu hingga muncul:

```
[WindowComparison] Dua query aktif.
[WindowComparison] Spark UI: http://localhost:4040
[WindowComparison] Tekan Ctrl+C untuk berhenti.
```

---

### Langkah A.5 — Amati output selama 4 menit

Perhatikan:
1. Berapa baris yang muncul pada output **tumbling** per trigger?
2. Berapa baris yang muncul pada output **sliding** per trigger?
3. Untuk periode waktu yang sama (misal 10:00–10:02), apakah nilai total berbeda antara tumbling dan sliding?

Catat pada **Tabel A.1** dan **Tabel A.2**.

Hentikan dengan `Ctrl+C` setelah 4 menit.

---

## Bagian B — Analisis Delivery Semantics

### Langkah B.1 — Tinjau script consumer analisis

Buka dan baca `Konfigurasi-lab/scripts/consumer_semantics.py`. Script ini:
- Membaca 100 event dari topic `transaksi-stream`
- Mendeteksi duplikat berdasarkan `event_id`
- Menggunakan `enable_auto_commit=False` dengan commit manual

---

### Langkah B.2 — (Opsional) Seed data uji duplikat

Agar analisis duplikat bermakna, kirim dataset khusus ke topic `transaksi-stream` (hentikan producer live terlebih dahulu jika perlu):

```bash
cd ../Konfigurasi-lab
source .venv/bin/activate
python scripts/seed_kafka.py \
  --topic transaksi-stream \
  --file data/transaksi_duplikat_test.json \
  --delay 0.0
```

File ini berisi 50 event dengan 10 `event_id` duplikat. Detail ada di [Data/README.md](../Data/README.md).

---

### Langkah B.3 — Jalankan consumer analisis

```bash
cd ../Konfigurasi-lab
source .venv/bin/activate
python scripts/consumer_semantics.py
```

Tunggu hingga 100 event terbaca dan ringkasan `RINGKASAN ANALISIS DELIVERY SEMANTICS` muncul. Catat semua angka pada **Tabel B.1**.

---

### Langkah B.4 — Jalankan ulang consumer (group yang sama)

Jalankan ulang script yang sama **tanpa perubahan**:

```bash
python scripts/consumer_semantics.py
```

Perhatikan apakah consumer membaca event yang sama (karena offset sudah di-commit) atau membaca event baru dari offset terakhir.

Catat perbedaan pada **Tabel B.2**.

---

## Tabel Pencatatan Hasil

### Tabel A.1 — Output Tumbling Window (2 menit)

*(catat dari minimal 3 trigger berbeda)*

| Trigger ke- | Waktu Trigger | Jumlah Baris Output | Rentang Window yang Muncul |
|---|---|---|---|
| 1 | _HH:MM:SS_ | _..._ | _..._ |
| 2 | _HH:MM:SS_ | _..._ | _..._ |
| 3 | _HH:MM:SS_ | _..._ | _..._ |
| **Rata-rata baris per trigger** | — | **_..._** | — |

### Tabel A.2 — Output Sliding Window (2 menit, slide 1 menit)

*(catat dari minimal 3 trigger berbeda)*

| Trigger ke- | Waktu Trigger | Jumlah Baris Output | Rentang Window yang Muncul |
|---|---|---|---|
| 1 | _HH:MM:SS_ | _..._ | _..._ |
| 2 | _HH:MM:SS_ | _..._ | _..._ |
| 3 | _HH:MM:SS_ | _..._ | _..._ |
| **Rata-rata baris per trigger** | — | **_..._** | — |

### Tabel A.3 — Perbandingan Tumbling vs Sliding

| Aspek Perbandingan | Tumbling (2 menit) | Sliding (2 menit / 1 menit) |
|---|---|---|
| Rata-rata baris per trigger | _..._ | _..._ |
| Satu event masuk ke berapa window? | **1** | **_..._ (maks 2)** |
| Apakah window bisa overlap? | Tidak | Ya / Tidak |
| Frekuensi window baru dibuat | Setiap 2 menit | Setiap _..._ menit |
| Overhead komputasi relatif | Lebih rendah / tinggi | Lebih rendah / tinggi |

### Tabel B.1 — Ringkasan Analisis Delivery Semantics (Run ke-1)

| Metrik | Nilai |
|---|---|
| Total event dibaca | _..._ |
| Event ID unik | _..._ |
| Duplikat terdeteksi | _..._ |
| Rasio duplikat | _..._ % |
| Channel dengan event terbanyak | _..._ |
| Persentase channel terbanyak | _..._ % |

### Tabel B.2 — Perbandingan Run ke-1 vs Run ke-2

| Aspek | Run ke-1 | Run ke-2 |
|---|---|---|
| Offset awal pembacaan | _..._ | _..._ |
| Apakah membaca event yang sama? | Ya / Tidak | — |
| Total event dibaca | 100 | _..._ |
| Apakah ada duplikat antar-run? | — | Ya / Tidak |

---

## Bagian C — Pertanyaan Diskusi Konseptual

Jawab pertanyaan berikut berdasarkan teori di modul dan pengamatan dari Latihan 1–5.

---

**C.1 — Pada Latihan 3, Query 1 menggunakan `outputMode("update")` sedangkan Query 2 menggunakan `outputMode("complete")`. Mengapa Query 2 tidak bisa menggunakan mode `update`? Apa yang terjadi jika Anda mencoba mengubahnya?**

> Tulis jawaban Anda di sini:
>
> _..._

---

**C.2 — Ketika pipeline di-restart pada Latihan 4, Spark membaca kembali dari offset checkpoint. Jika producer terus mengirim event selama Spark berhenti, apakah event-event tersebut hilang? Jelaskan mekanisme apa yang memastikan event tidak hilang.**

> Tulis jawaban Anda di sini:
>
> _..._

---

**C.3 — Jika event out-of-order (event_time lebih lama dari event terbaru) tiba setelah watermark sudah melewati window yang seharusnya, apa yang terjadi? Apakah event akan dimasukkan ke hasil agregasi?**

> Petunjuk: Kaitkan dengan konsep event lag, watermark, dan mekanisme "tutup window".
> Tulis jawaban Anda di sini:
>
> _..._

---

**C.4 — Mengapa jumlah consumer dalam satu consumer group yang lebih besar dari jumlah partisi justru tidak meningkatkan throughput? Apa trade-off dalam memilih jumlah partisi topic Kafka?**

> Petunjuk: Aturan fundamental: satu partisi hanya bisa dibaca oleh satu consumer dalam satu group.
> Tulis jawaban Anda di sini:
>
> _..._

---

**C.5 — Bandingkan overhead checkpoint antara query dengan window aggregation (Query 1) dan query tanpa window (Query 2 — global groupBy). Mana yang lebih berat secara komputasi? Mengapa?**

> Petunjuk: Pikirkan tentang berapa banyak state yang harus disimpan di setiap kasus.
> Tulis jawaban Anda di sini:
>
> _..._

---

## Refleksi dan Analisis

**R5.1 — Dari Tabel A.3, sliding window menghasilkan lebih banyak baris output per trigger. Dalam konteks bisnis nyata (misalnya: memantau transaksi mencurigakan setiap 5 menit dengan data 10 menit terakhir), kapan sliding window lebih tepat digunakan dibandingkan tumbling window?**

> Tulis jawaban Anda di sini:
>
> _..._

---

**R5.2 — Dari Tabel B.1, apakah ada duplikat yang terdeteksi dalam 100 event pertama? Jika tidak ada duplikat, apakah itu berarti producer menggunakan exactly-once semantics? Jelaskan perbedaan antara "tidak ada duplikat yang terdeteksi" dan "exactly-once dijamin".**

> Tulis jawaban Anda di sini:
>
> _..._

---

**R5.3 — Dari Tabel B.2, setelah run ke-1 selesai dengan `consumer.commit()`, run ke-2 tidak membaca event yang sama. Ini menunjukkan perilaku at-least-once atau at-most-once? Kapan duplikasi bisa terjadi pada konfigurasi ini?**

> Petunjuk: Pikirkan skenario: consumer crash setelah `consumer.commit()` tapi sebelum menyimpan hasil ke database.
> Tulis jawaban Anda di sini:
>
> _..._

---

**R5.4 — Dari seluruh rangkaian latihan (1–5), gambarkan arsitektur pipeline yang telah Anda bangun dalam format teks sederhana. Sertakan: sumber data → broker → processing → sink. Tambahkan mekanisme fault tolerance di setiap lapisan.**

> Contoh format:
> ```
> [Producer Python] → (key-based routing) → [Kafka: 3 partisi]
>        ↓ (offset tracking)
> [Spark Structured Streaming]
>        ↓ (checkpointing ke /tmp/)
> [Console Sink]
> ```
> Gambarkan versi lengkap dengan komponen fault tolerance:
>
> _..._

---

**R5.5 — Refleksi akhir: Dari semua konsep yang dipelajari di modul ini (batch vs streaming, Kafka, partitioning, delivery semantics, windowing, fault tolerance), konsep mana yang menurut Anda paling kritis untuk dipahami sebelum membangun sistem data real-time di lingkungan produksi? Berikan alasan berdasarkan pengalaman praktikum ini.**

> Tulis jawaban Anda di sini:
>
> _..._

---

## Tabel Rangkuman Seluruh Latihan

Isi tabel ini sebagai rangkuman komprehensif dari Latihan 1 sampai 5:

| Komponen | Konfigurasi yang Digunakan | Fungsi dalam Pipeline |
|---|---|---|
| Kafka Broker | KRaft, `modul8-kafka-broker`, port 9092 | _..._ |
| Topic `transaksi-stream` | 3 partisi, RF=1 | _..._ |
| Producer Python | `acks=all`, idempotent | _..._ |
| Message Key | `user_id` | _..._ |
| Spark Structured Streaming | local[2], micro-batch | _..._ |
| Tumbling Window | 1 menit (Latihan 3) | _..._ |
| Watermark | 2 menit | _..._ |
| Output Mode update | Query 1 | _..._ |
| Output Mode complete | Query 2 | _..._ |
| Checkpoint | `/tmp/checkpoints/` | _..._ |

---

## Kesimpulan Latihan 5

Setelah menyelesaikan seluruh rangkaian latihan Chapter 10, lengkapi pernyataan berikut:

> "Sliding window menghasilkan **___** kali lebih banyak output dibandingkan tumbling window karena setiap event bisa masuk ke **___** window yang berbeda. Consumer dengan `enable_auto_commit=False` dan commit manual menerapkan semantics **___** (at-most-once / at-least-once / exactly-once), sehingga duplikasi bisa terjadi jika consumer **___** setelah proses tapi sebelum commit. Untuk menjamin exactly-once end-to-end, diperlukan kombinasi: idempotent producer + **___** di Spark + **___** write di sink."

---

## Penutup Chapter 10

Ringkasan pencapaian setelah lima latihan:

| Latihan | Topik | Status |
|---|---|---|
| Latihan 1 | Setup lingkungan Kafka, verifikasi topic dan CLI | ☐ Selesai |
| Latihan 2 | Producer Python, key-based partitioning, format JSON | ☐ Selesai |
| Latihan 3 | Spark Streaming, tumbling window, dual query, Spark UI | ☐ Selesai |
| Latihan 4 | Fault tolerance, checkpoint, recovery tanpa kehilangan event | ☐ Selesai |
| Latihan 5 | Sliding vs tumbling, delivery semantics, diskusi konseptual | ☐ Selesai |

---

*Latihan 5 selesai. Chapter 10 praktik tuntas.*