# Latihan 2 — Producer Python: Simulasi Event Transaksi
**Chapter 10 · Analitik Aliran Data** | Estimasi waktu: **20 menit**

---

## Tujuan Latihan

Setelah menyelesaikan latihan ini, mahasiswa mampu:
- Menulis dan menjalankan producer Python menggunakan library `kafka-python`
- Memahami peran message key dalam penentuan partisi
- Mengamati distribusi pesan ke partisi-partisi Kafka
- Memverifikasi format payload JSON event yang diterima Kafka
- Mengidentifikasi konfigurasi producer untuk delivery semantics yang kuat

---

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Latihan 1 sudah selesai dan stack Kafka berjalan
- [ ] `docker compose ps` (dari `Konfigurasi-lab/`) menampilkan `modul8-kafka-broker` status `Up (healthy)`
- [ ] Virtual environment aktif: `source ../Konfigurasi-lab/.venv/bin/activate`
- [ ] Schema event — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md): `event_id`, `user_id`, `product`, `channel`, `amount`, `event_time`

---

## Referensi data

| File | Volume | Penggunaan |
|------|--------|------------|
| `data/sample_events.json` | 10 | Inspeksi format sebelum producer live |
| `data/transaksi_historis.json` | **100** | Seed historis via `seed_kafka.py` |

Mapping kanonik: `user_id` ↔ `PK-0001`, `product` ↔ `kelas_layanan`, `amount` ↔ `nilai_total`.

---

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Folder kerja | `Konfigurasi-lab/` |
| Producer script | `scripts/producer_transaksi.py` |
| Kafka broker | `modul8-kafka-broker` |
| Kafka UI | http://localhost:8080 |

> Semua perintah di latihan ini dijalankan dari folder **`Konfigurasi-lab/`** dengan venv aktif.

---

## Langkah Kerja

### Langkah 2.1 — Tinjau kode producer sebelum dijalankan

Buka dan baca file `Konfigurasi-lab/scripts/producer_transaksi.py`. Perhatikan bagian-bagian berikut sebelum menjalankannya:

```python
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8") if k else None,
    acks="all",                  # ← semua ISR harus konfirmasi
    enable_idempotence=True,     # ← cegah duplikat akibat retry
    retries=3,
)
```

Dan perhatikan fungsi `buat_event()` yang menentukan struktur setiap event:

```python
return {
    "event_id":   str(uuid.uuid4())[:8],   # ← ID unik 8 karakter
    "user_id":    user_id,                  # ← juga digunakan sebagai key
    "product":    random.choice(PRODUCTS),
    "channel":    random.choice(CHANNELS),
    "amount":     round(random.uniform(10_000, 5_000_000), 2),
    "event_time": event_time.isoformat(),
}, user_id  # ← user_id dikirim sebagai message key
```

> **Mengapa `user_id` dijadikan key?** Kafka menggunakan hash dari key untuk menentukan partisi tujuan. Semua transaksi dari user yang sama akan selalu masuk ke partisi yang sama, menjamin urutan pemrosesan per pengguna.

---

### Langkah 2.2 — Jalankan producer

Buka terminal baru (Terminal 1), masuk ke folder lab, aktifkan venv, lalu jalankan:

```bash
cd ../Konfigurasi-lab
source .venv/bin/activate
python scripts/producer_transaksi.py
```

Biarkan producer berjalan. Output yang muncul setiap 10 event (format angka `amount` dapat berbeda):

```
[10] id=3a9f21b0 user=usr-0023 amount=872345.12
[20] id=7c1e44f2 user=usr-0007 amount=1204000.45
...
```

Catat waktu mulai producer pada **Tabel 2.1**.

---

### Langkah 2.3 — Verifikasi event masuk ke Kafka via CLI

Buka terminal baru (Terminal 2) dan jalankan:

```bash
docker exec modul8-kafka-broker kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic transaksi-stream \
  --from-beginning \
  --max-messages 5
```

Amati **5 event pertama** yang muncul. Perhatikan format JSON-nya.

---

### Langkah 2.4 — Amati distribusi partisi via Kafka UI

Buka browser ke `http://localhost:8080`, navigasi ke:

**Topics → transaksi-stream → Overview**

Amati grafik **Messages per Partition**. Setelah producer berjalan ~2 menit, catat jumlah pesan di setiap partisi.

Kemudian navigasi ke:

**Topics → transaksi-stream → Messages**

Klik beberapa pesan dan amati field **Partition** dan **Offset** di detail pesan.

---

### Langkah 2.5 — Cek distribusi offset per partisi via CLI

Jalankan perintah berikut untuk melihat jumlah pesan yang tersimpan di setiap partisi:

```bash
docker exec modul8-kafka-broker kafka-run-class.sh kafka.tools.GetOffsetShell \
  --bootstrap-server localhost:9092 \
  --topic transaksi-stream
```

**Contoh output:**

```
transaksi-stream:0:87
transaksi-stream:1:84
transaksi-stream:2:89
```

Format: `topic:partisi:jumlah-offset`

Catat angka-angka ini pada **Tabel 2.2**. Ulangi perintah ini setelah 1 menit untuk melihat pertambahannya.

---

### Langkah 2.6 — Verifikasi key-based partitioning

Pilih satu `user_id` dari output producer, misalnya `usr-0015`. Kemudian filter pesan dari user tersebut di Kafka UI:

**Topics → transaksi-stream → Messages → Filter by key: `usr-0015`**

Catat nomor partisi dari **semua pesan** dengan key tersebut. Apakah semua masuk ke partisi yang sama?

---

### Langkah 2.7 — Hentikan producer setelah ~3 menit

Kembali ke Terminal 1 dan tekan `Ctrl+C`. Perhatikan pesan shutdown:

```
Producer dihentikan, total=342
```

Catat total event yang terkirim pada **Tabel 2.1**.

---

## Tabel Pencatatan Hasil

### Tabel 2.1 — Ringkasan Pengiriman Event

| Informasi | Nilai yang Tercatat |
|---|---|
| Waktu mulai producer | _HH:MM:SS_ |
| Waktu selesai producer | _HH:MM:SS_ |
| Total durasi berjalan | _menit:detik_ |
| Total event terkirim | _(dari pesan shutdown)_ |
| Rata-rata event per detik | _(hitung: total / durasi)_ |

### Tabel 2.2 — Distribusi Event per Partisi

| Partisi | Offset Awal (T=0) | Offset setelah 1 menit (T=1) | Pertambahan |
|---|---|---|---|
| Partisi 0 | _..._ | _..._ | _..._ |
| Partisi 1 | _..._ | _..._ | _..._ |
| Partisi 2 | _..._ | _..._ | _..._ |
| **Total** | _..._ | _..._ | _..._ |

### Tabel 2.3 — Verifikasi Format Event

Salin satu event JSON dari output CLI (Langkah 2.3) dan tempelkan di bawah:

```json
(tempel event JSON di sini)
```

Kemudian isi tabel validasi berikut:

| Field | Ada? | Tipe Data | Contoh Nilai |
|---|---|---|---|
| `event_id` | Ya/Tidak | _..._ | _..._ |
| `user_id` | Ya/Tidak | _..._ | _..._ |
| `product` | Ya/Tidak | _..._ | _..._ |
| `channel` | Ya/Tidak | _..._ | _..._ |
| `amount` | Ya/Tidak | _..._ | _..._ |
| `event_time` | Ya/Tidak | _..._ | _..._ |

### Tabel 2.4 — Verifikasi Key-Based Partitioning

Pilih satu `user_id` dan catat partisi dari minimal 3 pesannya:

| user_id yang dipilih | Pesan ke- | Offset | Partisi |
|---|---|---|---|
| _usr-xxxx_ | 1 | _..._ | _..._ |
| _usr-xxxx_ | 2 | _..._ | _..._ |
| _usr-xxxx_ | 3 | _..._ | _..._ |
| Apakah semua di partisi yang sama? | **Ya / Tidak** | — | — |

---

## Refleksi dan Analisis

**R2.1 — Dari Tabel 2.2, apakah distribusi pesan antar partisi merata? Mengapa distribusinya bisa tidak persis sama meskipun menggunakan key-based partitioning?**

> Petunjuk: Pikirkan tentang distribusi `user_id` yang dihasilkan `random.choice()` dan fungsi hash Kafka.
> Tulis jawaban Anda di sini:
>
> _..._

---

**R2.2 — Producer dikonfigurasi dengan `acks="all"` dan `enable_idempotence=True`. Jelaskan apa yang terjadi secara internal jika jaringan antara producer dan broker tiba-tiba terputus sesaat setelah pesan dikirim tetapi sebelum konfirmasi diterima.**

> Petunjuk: Hubungkan dengan konsep delivery semantics (at-least-once vs exactly-once) yang dijelaskan di modul.
> Tulis jawaban Anda di sini:
>
> _..._

---

**R2.3 — Pada Tabel 2.4, Anda membuktikan bahwa semua pesan dari user yang sama selalu masuk ke partisi yang sama. Apa keuntungan dan kerugian dari strategi ini dibandingkan round-robin (tanpa key)?**

> Petunjuk: Pikirkan tentang urutan pemrosesan, paralelisme, dan distribusi beban.
> Tulis jawaban Anda di sini:
>
> _..._

---

**R2.4 — Format `event_time` yang dihasilkan producer menggunakan `.isoformat()` dari Python, menghasilkan string seperti `"2024-04-15T10:23:45.123456+00:00"`. Mengapa format timestamp ini penting dalam sistem streaming? Apa yang terjadi jika dua event dari sumber berbeda menggunakan timezone yang berbeda?**

> Tulis jawaban Anda di sini:
>
> _..._

---

**R2.5 — Producer menggunakan `user_id` sebagai message key sehingga event dari user yang sama selalu masuk ke partisi yang sama. Jelaskan apa yang akan terjadi pada event out-of-order (event_time lebih lama dari event terbaru) saat diproses oleh Spark Structured Streaming dengan watermark. Apakah event akan selalu diproses?**

> Petunjuk: Baca kembali subbab 2.7 tentang Watermark dan Late Data.
> Tulis jawaban Anda di sini:
>
> _..._

---

## Kesimpulan Latihan 2

Setelah menyelesaikan latihan ini, lengkapi pernyataan berikut:

> "Producer Python mengirim event ke topic `transaksi-stream` dengan rata-rata **___** event/detik. Distribusi ke **___** partisi dilakukan berdasarkan **___** (hash key / round-robin). Terbukti bahwa semua event dari user yang sama masuk ke partisi **___** (berbeda/sama). Konfigurasi `enable_idempotence=True` memastikan delivery semantics **___** (at-most-once / at-least-once / exactly-once) di sisi producer."

---

*Latihan 2 selesai. Lanjutkan ke **Latihan 3 — Spark Structured Streaming: Agregasi Window**.*