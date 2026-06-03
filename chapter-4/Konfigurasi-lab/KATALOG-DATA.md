# Katalog Data — Chapter 4

Dataset latihan berupa **file teks** (bukan tabel) untuk operasi HDFS dan MapReduce WordCount. Kosakata selaras dengan entitas sintesis generator Copula (`partisipan`, `aktivitas`, `saluran`, `unit geografis`) — lihat [`synthetic-data/`](../../synthetic-data/README.md).

## File sumber

| Path | Format | Volume | Penggunaan |
|------|--------|--------|------------|
| `data/latihan.txt` | Teks bebas (kalimat) | **7 baris** | Latihan 3 — upload HDFS, fsck |
| `data/dataset_wordcount.txt` | Token per baris (spasi) | **6 baris** | Latihan 4–5 — input MapReduce |

## Isi `latihan.txt`

Narasi campuran **konsep Hadoop/HDFS** dan **kosakata platform partisipan** (selaras Bab 3+):

1. Platform partisipan & saluran interaksi
2. HDFS & blok 128MB
3. MapReduce & log aktivitas
4. Pipeline bronze → silver → gold
5. NameNode & metadata
6. DataNode & replikasi
7. Unit geografis (Jakarta, Surabaya, Bandung)

## Isi `dataset_wordcount.txt`

Enam baris token untuk WordCount. Kosakata dominan:

| Kategori | Contoh token |
|----------|--------------|
| Entitas sintesis | `partisipan`, `aktivitas`, `saluran` |
| Saluran | `mobile`, `web`, `qris`, `marketplace` |
| Kelas layanan | `elektronik`, `fashion`, `makanan` |
| Geografis | `jakarta`, `surabaya`, `bandung`, `medan` |
| Medallion | `bronze`, `silver`, `gold` |
| Hadoop | `hadoop`, `hdfs`, `mapreduce`, `namenode`, `datanode` |

### Frekuensi kata yang diharapkan (WordCount)

Setelah job MapReduce sukses, kata dengan frekuensi tinggi antara lain:

| Kata | Frekuensi (harapan) |
|------|---------------------|
| `partisipan` | 6 |
| `aktivitas` | 6 |
| `saluran` | 5 |
| `mobile` | 4 |
| `hadoop` | 2 |
| `hdfs` | 2 |
| `mapreduce` | 2 |

Gunakan tabel ini untuk memverifikasi output `part-r-00000`.

## Path HDFS

| Path | Sumber lokal |
|------|--------------|
| `/user/latihan/latihan.txt` | `data/latihan.txt` |
| `/user/latihan/input/dataset_wordcount.txt` | `data/dataset_wordcount.txt` |
| `/user/latihan/output/part-r-00000` | Hasil reduce WordCount |

## Regenerasi data

```bash
cd sesi-praktikum/synthetic-data
bash scripts/generate.sh ch04_hadoop
bash scripts/sync_to_chapters.sh
```
