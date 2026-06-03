# Latihan 4 — Pipeline ML End-to-End
**Chapter 11 · Machine Learning Big Data** | Estimasi waktu: **15 menit**

## Prasyarat

- [ ] Setup lab selesai — lihat [Konfigurasi-lab/README.md](../Konfigurasi-lab/README.md)
- [ ] Latihan 1–3 selesai
- [ ] Dataset & label — [KATALOG-DATA.md](../Konfigurasi-lab/KATALOG-DATA.md)

## Referensi Lingkungan Lab

| Item | Nilai |
|---|---|
| Folder kerja | `Konfigurasi-lab/` |
| Pipeline training | `scripts/pipeline_ml_e2e.py` |
| Inference | `scripts/inference.py` |
| Model path | `hdfs:///models/segmentasi_dt/v1` |
| Prediksi Gold | `hdfs:///datalake/gold/prediksi_segmen/` |

## Langkah Kerja

### 1) Jalankan pipeline end-to-end

```bash
cd ../Konfigurasi-lab
bash scripts/spark_submit.sh /opt/modul9/scripts/pipeline_ml_e2e.py
```

Catat:
- metrik training/test
- gap accuracy train-test
- durasi total

### 2) Verifikasi model dan output prediksi

```bash
docker exec bigdata-spark hdfs dfs -ls /models/segmentasi_dt/v1/
docker exec bigdata-spark hdfs dfs -du -h /models/segmentasi_dt/v1/
docker exec bigdata-spark hdfs dfs -ls /datalake/gold/prediksi_segmen/
```

### 3) Jalankan inference batch

```bash
cd ../Konfigurasi-lab
bash scripts/spark_submit.sh /opt/modul9/scripts/inference.py
```

Catat distribusi prediksi (`pred_idx`) dan contoh output.

---

*Latihan 4 selesai. Lanjut ke **Latihan 5 — Eksplorasi: Regularisasi, Kedalaman Pohon, dan Diskusi**.*
