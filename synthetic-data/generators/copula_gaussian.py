#!/usr/bin/env python3
"""
Generator data sintesis berbasis Gaussian Copula.

Membaca config/schema_v1.yaml dan mengekspor CSV/JSON per modul praktikum.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import uuid
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from scipy.stats import norm

# ---------------------------------------------------------------------------
# Konstanta & pool lookup
# ---------------------------------------------------------------------------

NAME_POOL = [
    "Andi Saputra", "Budi Santoso", "Sari Dewi", "Ahmad Rizky", "Maria Chen",
    "Dewi Lestari", "Budi Hartono", "Citra Dewi", "Dimas Pratama", "Eka Rahayu",
    "Fajar Nugroho", "Gita Lestari", "Hendra Wijaya", "Indah Permata", "Joko Santoso",
    "Kartika Sari", "Lukman Hakim", "Maya Putri", "Nanda Pratama", "Oki Ramadhan",
]

ITEMS_BY_KELAS: dict[str, list[str]] = {
    "elektronik": ["Laptop", "Mouse", "Headphone", "Tablet", "Charger", "Kabel"],
    "fashion": ["Kemeja", "Sepatu", "Celana", "Tas", "Jaket", "Topi"],
    "makanan": ["Kopi", "Teh", "Snack", "Beras", "Minyak", "Gula"],
    "kesehatan": ["Vitamin", "Masker", "Handsanitizer", "Obat Flu", "Termometer"],
    "otomotif": ["Oli", "Ban", "Aki", "Filter Udara", "Wiper"],
    "olahraga": ["Sepatu Lari", "Matras Yoga", "Dumbell", "Raket", "Jersey"],
}

PRICE_RANGE_BY_KELAS: dict[str, tuple[float, float]] = {
    "elektronik": (250_000, 8_500_000),
    "fashion": (45_000, 800_000),
    "makanan": (15_000, 150_000),
    "kesehatan": (25_000, 500_000),
    "otomotif": (50_000, 3_000_000),
    "olahraga": (75_000, 2_500_000),
}

SEGmen_TO_CH06 = {"regular": "Regular", "loyal": "Premium", "prioritas": "VIP"}
SEGmen_TO_CH08 = {"regular": "Regular", "loyal": "Premium", "prioritas": "Basic"}

KELAS_TITLE = {
    "elektronik": "Elektronik",
    "fashion": "Fashion",
    "makanan": "Makanan",
    "kesehatan": "Kesehatan",
    "otomotif": "Otomotif",
    "olahraga": "Olahraga",
}

DATE_MIN = date(2018, 1, 1)
DATE_MAX = date(2024, 6, 30)
AKTIVITAS_DATE_MIN = date(2024, 1, 1)
AKTIVITAS_DATE_MAX = date(2024, 12, 31)

# Teks Bab 4 — selaras kosakata entitas sintesis (tanpa label domain industri)
CH04_LATIHAN_LINES = [
    "Platform partisipan mencatat aktivitas transaksi melalui berbagai saluran interaksi.",
    "HDFS menyimpan catatan mentah dalam blok berukuran 128MB di klaster terdistribusi.",
    "MapReduce memproses log aktivitas partisipan secara paralel pada setiap node.",
    "Pipeline bronze silver gold mengolah data dari ingest mentah hingga ringkasan analitik.",
    "NameNode menyimpan metadata lokasi blok file sistem terdistribusi HDFS.",
    "DataNode menyimpan replikasi blok catatan aktivitas di setiap node fisik klaster.",
    "Unit geografis Jakarta Surabaya Bandung menerima volume aktivitas partisipan tertinggi.",
]

CH04_WORDCOUNT_LINES = [
    "partisipan aktivitas saluran mobile web partisipan jakarta",
    "elektronik fashion makanan aktivitas saluran mobile partisipan",
    "hadoop hdfs mapreduce partisipan aktivitas saluran bronze silver",
    "namenode datanode hdfs blok replikasi catatan aktivitas hadoop",
    "mapreduce mapper reducer aktivitas partisipan saluran mobile web",
    "qris marketplace saluran mobile aktivitas partisipan surabaya bandung medan",
]


# ---------------------------------------------------------------------------
# Gaussian Copula engine
# ---------------------------------------------------------------------------


class GaussianCopula:
    """Sampling multivariat via Gaussian Copula."""

    def __init__(self, rng: np.random.Generator):
        self.rng = rng

    @staticmethod
    def nearest_psd(matrix: np.ndarray, eps: float = 1e-8) -> np.ndarray:
        """Koreksi matriks ke positive semi-definite (eigenvalue clipping)."""
        sym = (matrix + matrix.T) / 2.0
        eigvals, eigvecs = np.linalg.eigh(sym)
        eigvals = np.clip(eigvals, eps, None)
        psd = eigvecs @ np.diag(eigvals) @ eigvecs.T
        d = np.sqrt(np.diag(psd))
        d[d == 0] = 1.0
        psd = psd / np.outer(d, d)
        np.fill_diagonal(psd, 1.0)
        return psd

    def sample_uniform(self, n: int, corr: np.ndarray) -> np.ndarray:
        """Sample n × d pseudo-observasi uniform dari Gaussian Copula."""
        d = corr.shape[0]
        psd = self.nearest_psd(corr)
        z = self.rng.multivariate_normal(np.zeros(d), psd, size=n)
        return norm.cdf(z)

    @staticmethod
    def rank_uniform(values: np.ndarray) -> np.ndarray:
        """Transformasi rank-based ke (0, 1)."""
        n = len(values)
        ranks = np.argsort(np.argsort(values)) + 1
        return ranks / (n + 1)


# ---------------------------------------------------------------------------
# Pipeline sintesis
# ---------------------------------------------------------------------------


class SyntheticPipeline:
    """Orkestrasi generate entitas dari schema YAML."""

    def __init__(self, schema: dict[str, Any], seed: int = 42):
        self.schema = schema
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.copula = GaussianCopula(self.rng)
        self._partisipan: list[dict[str, Any]] = []
        self._unit_layanan: list[dict[str, Any]] = []
        self._aktivitas: list[dict[str, Any]] = []

    # --- helpers ---

    @staticmethod
    def _u_to_categorical(u: float, values: list[str], weights: list[float] | None = None) -> str:
        w = np.array(weights if weights else [1.0] * len(values), dtype=float)
        w /= w.sum()
        cum = np.cumsum(w)
        idx = int(np.searchsorted(cum, u, side="right"))
        idx = min(idx, len(values) - 1)
        return values[idx]

    @staticmethod
    def _u_to_date(u: float, dmin: date, dmax: date) -> date:
        span = (dmax - dmin).days
        return dmin + timedelta(days=int(u * span))

    @staticmethod
    def _segmen_label(code: int) -> str:
        mapping = {1: "regular", 2: "loyal", 3: "prioritas"}
        return mapping.get(int(np.clip(round(code), 1, 3)), "regular")

    @staticmethod
    def _uuid8() -> str:
        return uuid.uuid4().hex[:8]

    def _assign_weighted_fk(self, n: int, ids: list[str]) -> list[str]:
        """Zipf-like: sedikit partisipan high-volume."""
        weights = 1.0 / np.power(np.arange(1, len(ids) + 1), 0.8)
        weights /= weights.sum()
        return list(self.rng.choice(ids, size=n, replace=True, p=weights))

    # --- blok copula ---

    def _block_a_corr(self) -> np.ndarray:
        return np.array([
            [1.00, 0.10, 0.15, -0.05],
            [0.10, 1.00, 0.08, 0.00],
            [0.15, 0.08, 1.00, 0.12],
            [-0.05, 0.00, 0.12, 1.00],
        ])

    def _block_b_corr(self) -> np.ndarray:
        return np.array([
            [1.00, -0.15, 0.10, 0.00, 0.35, 0.05, 0.10],
            [-0.15, 1.00, 0.05, 0.08, -0.10, 0.10, 0.20],
            [0.10, 0.05, 1.00, -0.05, 0.00, 0.00, 0.00],
            [0.00, 0.08, -0.05, 1.00, 0.05, 0.10, 0.00],
            [0.35, -0.10, 0.00, 0.05, 1.00, 0.00, 0.05],
            [0.05, 0.10, 0.00, 0.10, 0.00, 1.00, 0.00],
            [0.10, 0.20, 0.00, 0.00, 0.05, 0.00, 1.00],
        ])

    def _block_c_corr(self) -> np.ndarray:
        return np.array([
            [1.00, 0.55, 0.45],
            [0.55, 1.00, 0.50],
            [0.45, 0.50, 1.00],
        ])

    def _block_d_corr(self) -> np.ndarray:
        target = self.schema.get("copula_blocks", {}).get("D", {}).get("target_correlation", 0.4)
        return np.array([[1.0, target], [target, 1.0]])

    # --- entity generators ---

    def generate_unit_layanan(self, n: int = 30) -> list[dict[str, Any]]:
        kelas_vals = self.schema["entities"]["unit_layanan"]["columns"]["kelas_layanan"]["values"]
        geo_vals = self.schema["entities"]["unit_layanan"]["columns"]["unit_geografis"]["values"]
        skala_vals = ["kecil", "sedang", "besar"]
        rows = []
        for i in range(1, n + 1):
            rows.append({
                "id_unit": f"UL-{i:03d}",
                "nama_unit": f"Unit-{i:03d}",
                "kelas_layanan": kelas_vals[(i - 1) % len(kelas_vals)],
                "unit_geografis": geo_vals[(i - 1) % len(geo_vals)],
                "skala_operasi": skala_vals[(i - 1) % len(skala_vals)],
            })
        self._unit_layanan = rows
        return rows

    def generate_partisipan(self, n: int) -> list[dict[str, Any]]:
        cfg = self.schema["entities"]["partisipan"]["columns"]
        tipe_vals = cfg["tipe_partisipan"]["values"]
        geo_vals = cfg["unit_geografis"]["values"]
        tipe_w = [0.45, 0.30, 0.20, 0.05]

        u = self.copula.sample_uniform(n, self._block_a_corr())
        rows = []
        for i in range(n):
            tipe = self._u_to_categorical(u[i, 0], tipe_vals, tipe_w)
            geo = self._u_to_categorical(u[i, 1], geo_vals)
            segmen = self._segmen_label(1 + u[i, 2] * 2.99)
            tgl = self._u_to_date(u[i, 3], DATE_MIN, DATE_MAX)
            pid = f"PK-{i + 1:04d}"
            rows.append({
                "id_partisipan": pid,
                "nama": NAME_POOL[i % len(NAME_POOL)],
                "tipe_partisipan": tipe,
                "unit_geografis": geo,
                "segmen": segmen,
                "tanggal_bergabung": tgl.isoformat(),
                "email": f"{pid.lower()}@lab.local",
                "usia": int(22 + (u[i, 2] * 33)),
                "pendapatan": int(5_000_000 + u[i, 0] * 15_000_000),
            })
        self._partisipan = rows
        return rows

    def generate_aktivitas(
        self,
        n: int,
        partisipan: list[dict[str, Any]] | None = None,
        units: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        partisipan = partisipan or self._partisipan
        units = units or self._unit_layanan
        if not partisipan:
            raise ValueError("Partisipan harus di-generate terlebih dahulu")
        if not units:
            self.generate_unit_layanan(max(10, len(partisipan)))
            units = self._unit_layanan

        kelas_vals = self.schema["entities"]["aktivitas"]["columns"]["kelas_layanan"]["values"]
        saluran_vals = self.schema["entities"]["aktivitas"]["columns"]["saluran"]["values"]
        status_vals = self.schema["entities"]["aktivitas"]["columns"]["status"]["values"]
        status_w = self.schema["entities"]["aktivitas"]["columns"]["status"]["default_weights"]

        pids = [p["id_partisipan"] for p in partisipan]
        pmap = {p["id_partisipan"]: p for p in partisipan}
        unit_ids = [u["id_unit"] for u in units]
        umap = {u["id_unit"]: u for u in units}

        assigned_p = self._assign_weighted_fk(n, pids)
        u = self.copula.sample_uniform(n, self._block_b_corr())

        rows = []
        for i in range(n):
            kelas = self._u_to_categorical(u[i, 4], kelas_vals)
            saluran = self._u_to_categorical(u[i, 5], saluran_vals)
            kuantitas = int(np.clip(round(1 + u[i, 1] * 19), 1, 20))
            rasio = float(np.clip(u[i, 2] * 0.3, 0.0, 0.3))
            lo, hi = PRICE_RANGE_BY_KELAS[kelas]
            harga = lo + u[i, 0] * (hi - lo)
            berat = float(np.clip(math.exp(math.log(0.1) + u[i, 6] * math.log(10.0 / 0.1)), 0.1, 10.0))
            tanggal = self._u_to_date(u[i, 3], AKTIVITAS_DATE_MIN, AKTIVITAS_DATE_MAX)
            nilai = round(kuantitas * harga * (1 - rasio), 2)

            pid = assigned_p[i]
            uid = unit_ids[i % len(unit_ids)]
            items = ITEMS_BY_KELAS[kelas]
            nama_item = items[i % len(items)]

            dt = datetime.combine(tanggal, datetime.min.time()).replace(tzinfo=timezone.utc)
            dt = dt + timedelta(seconds=int(u[i, 3] * 86400))

            rows.append({
                "id_aktivitas": f"ACT-{self._uuid8()}",
                "id_partisipan": pid,
                "id_unit_layanan": uid,
                "tanggal": tanggal.isoformat(),
                "event_time": dt.isoformat().replace("+00:00", "+00:00"),
                "kelas_layanan": kelas,
                "nama_item": nama_item,
                "saluran": saluran,
                "kuantitas": kuantitas,
                "harga_satuan": round(harga, 2),
                "rasio_penyesuaian": round(rasio, 4),
                "nilai_total": nilai,
                "berat_unit": round(berat, 2),
                "unit_geografis": pmap[pid]["unit_geografis"],
                "status": self._u_to_categorical(u[i, 0], status_vals, status_w),
                "tahun": tanggal.year,
                "bulan": tanggal.month,
            })
        self._aktivitas = rows
        return rows

    def generate_skor(self, n: int, partisipan: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        partisipan = partisipan or self._partisipan
        if not partisipan:
            self.generate_partisipan(max(n, 10))
            partisipan = self._partisipan[:n]

        u = self.copula.sample_uniform(n, self._block_c_corr())
        rows = []
        for i in range(n):
            p = partisipan[i % len(partisipan)]
            rows.append({
                "id_partisipan": p["id_partisipan"],
                "nama": p["nama"],
                "skor_modul_a": round(float(np.clip(40 + u[i, 0] * 55, 0, 100)), 1),
                "skor_modul_b": round(float(np.clip(40 + u[i, 1] * 55, 0, 100)), 1),
                "skor_modul_c": round(float(np.clip(40 + u[i, 2] * 55, 0, 100)), 1),
            })
        return rows

    def generate_sensor(self, n: int) -> list[dict[str, Any]]:
        lokasi_vals = self.schema["entities"]["sensor"]["columns"]["lokasi"]["values"]
        u = self.copula.sample_uniform(n, self._block_d_corr())
        rows = []
        base = datetime(2024, 4, 15, 8, 0, 0, tzinfo=timezone.utc)
        for i in range(n):
            suhu = float(20.0 + u[i, 0] * 25.0)
            kelembapan = float(30.0 + u[i, 1] * 60.0)
            if suhu > 40 or kelembapan > 85:
                status = "critical"
            elif suhu > 35 or kelembapan > 75:
                status = "warning"
            else:
                status = "normal"
            sid = f"sensor-{(i % 20) + 1:03d}"
            rows.append({
                "event_id": self._uuid8(),
                "sensor_id": sid,
                "lokasi": lokasi_vals[i % len(lokasi_vals)],
                "suhu": round(suhu, 2),
                "kelembapan": round(kelembapan, 2),
                "status": status,
                "event_time": (base + timedelta(seconds=i * 15)).isoformat(),
            })
        return rows

    @staticmethod
    def segmen_ml(nilai: float) -> str:
        if nilai < 100_000:
            return "rendah"
        if nilai < 1_000_000:
            return "menengah"
        return "tinggi"

    # --- anomali terkontrol ---

    def apply_ch06_anomalies(self, aktivitas: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows = deepcopy(aktivitas)
        if len(rows) < 5:
            return rows
        # duplicate PK
        dup = deepcopy(rows[0])
        dup["id_aktivitas"] = rows[0]["id_aktivitas"]
        rows.append(dup)
        # null FK
        rows[10 % len(rows)]["id_partisipan"] = ""
        # negative nilai
        rows[11 % len(rows)]["nilai_total"] = -150_000
        rows[11 % len(rows)]["harga_satuan"] = -150_000
        # zero kuantitas
        rows[12 % len(rows)]["kuantitas"] = 0
        # casing geografis
        rows[13 % len(rows)]["unit_geografis"] = rows[13 % len(rows)]["unit_geografis"].lower()
        return rows

    def apply_ch03_anomalies(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        out = deepcopy(rows)
        if len(out) >= 5:
            out.append(deepcopy(out[4]))  # duplikat Budi Santoso
        if len(out) >= 3:
            out[2]["pendapatan"] = None
        return out

    def apply_ch09_bad_rows(self, rows: list[dict[str, Any]], rate: float = 0.03) -> list[dict[str, Any]]:
        out = deepcopy(rows)
        n_bad = max(1, int(len(out) * rate))
        for i in range(n_bad):
            if i % 2 == 0:
                out[i]["id_aktivitas"] = ""
            else:
                out[i]["nilai_total"] = -float(out[i]["nilai_total"])
        return out

    # --- gold aggregates ---

    @staticmethod
    def compute_gold(aktivitas: list[dict[str, Any]], partisipan: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        from collections import defaultdict

        by_month: dict[tuple[int, int], dict[str, Any]] = defaultdict(
            lambda: {"omzet": 0.0, "n": 0, "pelanggan": set()}
        )
        by_kelas: dict[str, dict[str, Any]] = defaultdict(lambda: {"omzet": 0.0, "n": 0})
        by_geo: dict[str, dict[str, Any]] = defaultdict(lambda: {"omzet": 0.0, "n": 0, "pelanggan": set()})
        by_p: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"freq": 0, "monetary": 0.0, "last": None}
        )

        for row in aktivitas:
            if row.get("nilai_total", 0) <= 0:
                continue
            tgl = date.fromisoformat(row["tanggal"])
            key = (tgl.year, tgl.month)
            v = float(row["nilai_total"])
            by_month[key]["omzet"] += v
            by_month[key]["n"] += 1
            by_month[key]["pelanggan"].add(row["id_partisipan"])

            k = row["kelas_layanan"]
            by_kelas[k]["omzet"] += v
            by_kelas[k]["n"] += 1

            g = row["unit_geografis"]
            by_geo[g]["omzet"] += v
            by_geo[g]["n"] += 1
            by_geo[g]["pelanggan"].add(row["id_partisipan"])

            p = row["id_partisipan"]
            by_p[p]["freq"] += 1
            by_p[p]["monetary"] += v
            if by_p[p]["last"] is None or tgl > by_p[p]["last"]:
                by_p[p]["last"] = tgl

        ref = max((r["tanggal"] for r in aktivitas), default=AKTIVITAS_DATE_MAX.isoformat())
        ref_date = date.fromisoformat(ref)

        tren = []
        for (y, m), agg in sorted(by_month.items()):
            tren.append({
                "tahun": y,
                "bulan": m,
                "periode": f"{y}-{m:02d}",
                "omzet": round(agg["omzet"], 2),
                "jumlah_transaksi": agg["n"],
                "n_transaksi": agg["n"],
                "pelanggan_aktif": len(agg["pelanggan"]),
                "rata_transaksi": round(agg["omzet"] / agg["n"], 2) if agg["n"] else 0,
                "avg_nilai": round(agg["omzet"] / agg["n"], 2) if agg["n"] else 0,
            })

        total_omzet = sum(t["omzet"] for t in tren) or 1.0
        omzet_kelas = []
        for k, agg in sorted(by_kelas.items(), key=lambda x: -x[1]["omzet"]):
            omzet_kelas.append({
                "kategori": KELAS_TITLE.get(k, k),
                "kelas_layanan": k,
                "omzet_total": round(agg["omzet"], 2),
                "omzet": round(agg["omzet"], 2),
                "n_transaksi": agg["n"],
                "persen_omzet": round(100 * agg["omzet"] / total_omzet, 2),
            })

        omzet_geo = []
        for g, agg in sorted(by_geo.items(), key=lambda x: -x[1]["omzet"]):
            omzet_geo.append({
                "kota": g,
                "unit_geografis": g,
                "omzet": round(agg["omzet"], 2),
                "transaksi": agg["n"],
                "n_transaksi": agg["n"],
                "pelanggan_unik": len(agg["pelanggan"]),
            })

        rfm = []
        for pid, agg in by_p.items():
            recency = (ref_date - agg["last"]).days if agg["last"] else 999
            if agg["freq"] >= 20 and recency <= 30:
                seg = "Champion"
            elif agg["freq"] >= 10 and recency <= 60:
                seg = "Loyal"
            elif recency > 90:
                seg = "At Risk"
            else:
                seg = "Regular"
            rfm.append({
                "id_pelanggan": pid,
                "id_partisipan": pid,
                "frekuensi": agg["freq"],
                "frequency": agg["freq"],
                "monetary": round(agg["monetary"], 2),
                "last_purchase": agg["last"].isoformat() if agg["last"] else "",
                "recency_hari": recency,
                "recency": recency,
                "segmen_rfm": seg,
            })

        return {
            "tren_bulanan": tren,
            "omzet_kelas": omzet_kelas,
            "omzet_geografis": omzet_geo,
            "segmentasi_rfm": rfm,
        }

    @staticmethod
    def compute_tren_lanjutan(tren: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows = sorted(tren, key=lambda x: (x["tahun"], x["bulan"]))
        rank_order = sorted(range(len(rows)), key=lambda i: -float(rows[i]["omzet"]))
        rank = [0] * len(rows)
        for rnk, idx in enumerate(rank_order, 1):
            rank[idx] = rnk
        out = []
        kum = 0.0
        for i, r in enumerate(rows):
            omzet = float(r["omzet"])
            kum += omzet
            window = [float(rows[j]["omzet"]) for j in range(max(0, i - 2), i + 1)]
            ma3 = sum(window) / len(window)
            prev = float(rows[i - 1]["omzet"]) if i > 0 else None
            mom = round((omzet - prev) / prev * 100, 2) if prev else None
            out.append({
                **r,
                "ma3_omzet": round(ma3, 2),
                "omzet_bulan_lalu": round(prev, 2) if prev is not None else "",
                "mom_growth_pct": mom if mom is not None else "",
                "kumulatif_omzet": round(kum, 2),
                "peringkat_omzet": rank[i],
            })
        return out


# ---------------------------------------------------------------------------
# Export per modul
# ---------------------------------------------------------------------------


class ModuleExporter:
    """Format & tulis output CSV/JSON sesuai modul praktikum."""

    def __init__(self, pipeline: SyntheticPipeline, output_dir: Path):
        self.pipeline = pipeline
        self.output_dir = output_dir
        self.schema = pipeline.schema

    def _module_dir(self, module: str) -> Path:
        d = self.output_dir / module
        d.mkdir(parents=True, exist_ok=True)
        return d

    @staticmethod
    def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            w.writeheader()
            for row in rows:
                w.writerow({k: row.get(k, "") for k in fieldnames})

    @staticmethod
    def write_json(path: Path, rows: list[dict[str, Any]]) -> None:
        with path.open("w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
            f.write("\n")

    def _legacy_pelanggan_ch06(self, partisipan: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows = []
        for i, p in enumerate(partisipan):
            rows.append({
                "id_pelanggan": f"C{i + 1:03d}",
                "nama": p["nama"],
                "email": p["email"],
                "segmen": SEGmen_TO_CH06.get(p["segmen"], "Regular"),
                "tanggal_daftar": p["tanggal_bergabung"],
            })
        return rows

    def _legacy_pelanggan_ch08(self, partisipan: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows = []
        for i, p in enumerate(partisipan):
            rows.append({
                "id_pelanggan": f"PLG-{i + 1:04d}",
                "nama": p["nama"] if i < 20 else f"Pelanggan-{i + 1:04d}",
                "segmen": SEGmen_TO_CH08.get(p["segmen"], "Regular"),
                "kota_asal": p["unit_geografis"],
            })
        return rows

    def _legacy_transaksi_ch06(self, aktivitas: list[dict[str, Any]], partisipan: list[dict[str, Any]]) -> list[dict[str, Any]]:
        pid_map = {p["id_partisipan"]: f"C{i + 1:03d}" for i, p in enumerate(partisipan)}
        trx_id: dict[str, str] = {}
        counter = 1
        rows = []
        for a in aktivitas:
            aid = a["id_aktivitas"]
            if aid not in trx_id:
                trx_id[aid] = f"TRX{counter:03d}"
                counter += 1
            rows.append({
                "id_transaksi": trx_id[aid],
                "id_pelanggan": pid_map.get(a["id_partisipan"], ""),
                "tanggal": a["tanggal"],
                "kategori": KELAS_TITLE.get(a["kelas_layanan"], a["kelas_layanan"]),
                "produk": a["nama_item"],
                "jumlah": int(a["harga_satuan"]),
                "kuantitas": a["kuantitas"],
                "kota": a["unit_geografis"],
            })
        return rows

    def _legacy_transaksi_ch08(self, aktivitas: list[dict[str, Any]], partisipan: list[dict[str, Any]]) -> list[dict[str, Any]]:
        pid_map = {p["id_partisipan"]: f"PLG-{i + 1:04d}" for i, p in enumerate(partisipan)}
        rows = []
        for i, a in enumerate(aktivitas):
            rows.append({
                "id_transaksi": f"TRX-{i + 1:05d}",
                "id_pelanggan": pid_map.get(a["id_partisipan"], ""),
                "tanggal": a["tanggal"],
                "kategori": KELAS_TITLE.get(a["kelas_layanan"], a["kelas_layanan"]),
                "total_nilai": a["nilai_total"],
                "kota": a["unit_geografis"],
            })
        return rows

    def export_ch03_minio(self) -> None:
        cfg = self.schema["module_exports"]["ch03_minio"]
        n = cfg["n_rows"]
        rows = self.pipeline.generate_partisipan(n)
        rows = self.pipeline.apply_ch03_anomalies(rows)
        out = self._module_dir("ch03_minio")
        legacy = [{
            "id": i + 1,
            "name": r["nama"],
            "age": r["usia"],
            "city": r["unit_geografis"],
            "salary": r["pendapatan"],
            "join_date": r["tanggal_bergabung"],
        } for i, r in enumerate(rows)]
        self.write_csv(out / "sample_users.csv", legacy,
                       ["id", "name", "age", "city", "salary", "join_date"])
        self.write_csv(out / "entitas_partisipan.csv", rows,
                       list(rows[0].keys()) if rows else [])

    def export_ch05_spark(self) -> None:
        cfg = self.schema["module_exports"]["ch05_spark"]
        n = cfg["n_rows"]
        partisipan = self.pipeline.generate_partisipan(max(n, 10))
        skor = self.pipeline.generate_skor(n, partisipan)
        out = self._module_dir("ch05_spark")
        legacy = [{
            "nim": f"2021{i + 1:03d}",
            "nama": s["nama"],
            "nilai_uts": s["skor_modul_a"],
            "nilai_uas": s["skor_modul_b"],
            "nilai_tugas": s["skor_modul_c"],
        } for i, s in enumerate(skor)]
        self.write_csv(out / "mahasiswa.csv", legacy,
                       ["nim", "nama", "nilai_uts", "nilai_uas", "nilai_tugas"])
        self.write_csv(out / "skor_kompetensi.csv", skor, list(skor[0].keys()))

    def export_ch06_medallion(self) -> None:
        cfg = self.schema["module_exports"]["ch06_medallion"]
        n_p = cfg["n_rows"]["partisipan"]
        n_a = cfg["n_rows"]["aktivitas"]
        partisipan = self.pipeline.generate_partisipan(n_p)
        aktivitas = self.pipeline.generate_aktivitas(n_a, partisipan)
        aktivitas = self.pipeline.apply_ch06_anomalies(aktivitas)
        out = self._module_dir("ch06_medallion")
        trx = self._legacy_transaksi_ch06(aktivitas, partisipan)
        pel = self._legacy_pelanggan_ch06(partisipan)
        self.write_csv(out / "entitas_partisipan.csv", partisipan, list(partisipan[0].keys()))
        self.write_csv(
            out / "catatan_aktivitas.csv",
            aktivitas,
            [
                "id_aktivitas", "id_partisipan", "tanggal", "kelas_layanan", "nama_item",
                "saluran", "kuantitas", "harga_satuan", "nilai_total", "unit_geografis", "status",
            ],
        )
        self.write_csv(out / "transaksi.csv", trx,
                       ["id_transaksi", "id_pelanggan", "tanggal", "kategori", "produk", "jumlah", "kuantitas", "kota"])
        self.write_csv(out / "pelanggan.csv", pel,
                       ["id_pelanggan", "nama", "email", "segmen", "tanggal_daftar"])
        # ch07 uses identical files
        out7 = self._module_dir("ch07_medallion_local")
        self.write_csv(out7 / "transaksi.csv", trx,
                       ["id_transaksi", "id_pelanggan", "tanggal", "kategori", "produk", "jumlah", "kuantitas", "kota"])
        self.write_csv(out7 / "pelanggan.csv", pel,
                       ["id_pelanggan", "nama", "email", "segmen", "tanggal_daftar"])

    def export_ch08_storage(self) -> None:
        cfg = self.schema["module_exports"]["ch08_storage"]
        n_p = cfg["n_rows"]["partisipan"]
        n_a = cfg["n_rows"]["aktivitas"]
        partisipan = self.pipeline.generate_partisipan(n_p)
        aktivitas = self.pipeline.generate_aktivitas(n_a, partisipan)
        out = self._module_dir("ch08_storage")
        trx_rows = self._legacy_transaksi_ch08(aktivitas, partisipan)
        pel_rows = self._legacy_pelanggan_ch08(partisipan)
        self.write_csv(
            out / "entitas_partisipan.csv",
            partisipan,
            list(partisipan[0].keys()),
        )
        self.write_csv(
            out / "catatan_aktivitas.csv",
            [
                {
                    "id_aktivitas": a["id_aktivitas"],
                    "id_partisipan": a["id_partisipan"],
                    "tanggal": a["tanggal"],
                    "kelas_layanan": a["kelas_layanan"],
                    "total_nilai": a["nilai_total"],
                    "unit_geografis": a["unit_geografis"],
                    "saluran": a["saluran"],
                }
                for a in aktivitas
            ],
            ["id_aktivitas", "id_partisipan", "tanggal", "kelas_layanan", "total_nilai", "unit_geografis", "saluran"],
        )
        self.write_csv(out / "transaksi.csv", trx_rows,
                       ["id_transaksi", "id_pelanggan", "tanggal", "kategori", "total_nilai", "kota"])
        self.write_csv(out / "pelanggan.csv", pel_rows,
                       ["id_pelanggan", "nama", "segmen", "kota_asal"])

    def export_ch09_orchestration(self) -> None:
        cfg = self.schema["module_exports"]["ch09_orchestration"]
        n = cfg["n_rows"]
        partisipan = self.pipeline.generate_partisipan(30)
        aktivitas = self.pipeline.generate_aktivitas(n, partisipan)
        aktivitas = self.pipeline.apply_ch09_bad_rows(aktivitas, cfg.get("bad_row_rate", 0.03))
        out = self._module_dir("ch09_orchestration")
        subset = [{
            "id": a["id_aktivitas"],
            "nilai": a["nilai_total"],
            "kategori": a["kelas_layanan"],
        } for a in aktivitas]
        self.write_csv(out / "transaksi_harian.csv", subset, ["id", "nilai", "kategori"])
        self.write_csv(
            out / "catatan_aktivitas_harian.csv",
            [
                {
                    "id_aktivitas": a["id_aktivitas"],
                    "id_partisipan": a["id_partisipan"],
                    "tanggal": a["tanggal"],
                    "kelas_layanan": a["kelas_layanan"],
                    "nilai_total": a["nilai_total"],
                    "saluran": a["saluran"],
                    "unit_geografis": a["unit_geografis"],
                }
                for a in aktivitas
            ],
            ["id_aktivitas", "id_partisipan", "tanggal", "kelas_layanan", "nilai_total", "saluran", "unit_geografis"],
        )

    def export_ch10_streaming(self) -> None:
        cfg = self.schema["module_exports"]["ch10_streaming"]
        n_a = cfg["n_rows"]["aktivitas"]
        n_s = cfg["n_rows"]["sensor"]
        partisipan = self.pipeline.generate_partisipan(50)
        aktivitas = self.pipeline.generate_aktivitas(n_a, partisipan)
        sensor = self.pipeline.generate_sensor(n_s)
        alias = self.schema.get("streaming_alias", {})

        pid_idx = {p["id_partisipan"]: i + 1 for i, p in enumerate(partisipan)}
        stream_trx = []
        for a in aktivitas:
            idx = pid_idx.get(a["id_partisipan"], 1)
            stream_trx.append({
                "event_id": a["id_aktivitas"].replace("ACT-", "")[:8],
                alias.get("id_partisipan", "user_id"): f"usr-{idx:04d}",
                alias.get("kelas_layanan", "product"): a["kelas_layanan"],
                alias.get("saluran", "channel"): a["saluran"],
                alias.get("nilai_total", "amount"): a["nilai_total"],
                "event_time": a["event_time"],
            })

        stream_sensor = [{
            "event_id": s["event_id"],
            "sensor_id": s["sensor_id"],
            "location": s["lokasi"],
            "temperature": s["suhu"],
            "humidity": s["kelembapan"],
            "status": s["status"],
            "event_time": s["event_time"],
        } for s in sensor]

        out = self._module_dir("ch10_streaming")
        self.write_json(out / "transaksi_historis.json", stream_trx)
        self.write_json(out / "sample_events.json", stream_trx[:10])
        self.write_json(out / "sensor_iot_historis.json", stream_sensor)
        dup = deepcopy(stream_trx[:50])
        for i in range(10):
            dup[40 + i]["event_id"] = dup[i]["event_id"]
        self.write_json(out / "transaksi_duplikat_test.json", dup)
        self.write_json(
            out / "catatan_aktivitas_streaming.json",
            [
                {
                    "id_aktivitas": a["id_aktivitas"],
                    "id_partisipan": a["id_partisipan"],
                    "kelas_layanan": a["kelas_layanan"],
                    "nilai_total": a["nilai_total"],
                    "saluran": a["saluran"],
                    "unit_geografis": a["unit_geografis"],
                    "event_time": a["event_time"],
                }
                for a in aktivitas
            ],
        )
        self.write_json(
            out / "pembacaan_sensor.json",
            [
                {
                    "event_id": s["event_id"],
                    "sensor_id": s["sensor_id"],
                    "lokasi": s["lokasi"],
                    "suhu": s["suhu"],
                    "kelembapan": s["kelembapan"],
                    "status": s["status"],
                    "event_time": s["event_time"],
                }
                for s in sensor
            ],
        )

    def export_ch11_ml(self) -> None:
        cfg = self.schema["module_exports"]["ch11_ml"]
        n = cfg["n_rows"]
        n_p = cfg.get("n_partisipan", 200)
        partisipan = self.pipeline.generate_partisipan(n_p)
        aktivitas = self.pipeline.generate_aktivitas(n, partisipan)
        pid_idx = {p["id_partisipan"]: i + 1 for i, p in enumerate(partisipan)}

        ml_rows = []
        for a in aktivitas:
            idx = pid_idx.get(a["id_partisipan"], 1)
            q, h, d = a["kuantitas"], a["harga_satuan"], a["rasio_penyesuaian"]
            total = round(q * h * (1 - d), 2)
            ml_rows.append({
                "id_transaksi": a["id_aktivitas"].replace("ACT-", "")[:8],
                "id_pelanggan": f"usr-{idx:04d}",
                "kategori": a["kelas_layanan"],
                "channel": a["saluran"],
                "kuantitas": q,
                "harga_satuan": h,
                "diskon": d,
                "total_nilai": total,
                "berat_kg": a["berat_unit"],
                "segmen": self.pipeline.segmen_ml(float(total)),
            })

        out = self._module_dir("ch11_ml")
        self.write_csv(out / "transaksi_ml.csv", ml_rows, list(ml_rows[0].keys()))
        self.write_json(out / "transaksi_ml.json", ml_rows)

        from collections import defaultdict

        agg: dict[str, dict] = defaultdict(
            lambda: {"total_trx": 0, "total_belanja": 0.0, "maks_belanja": 0.0, "kategori": set()}
        )
        for r in ml_rows:
            p = r["id_pelanggan"]
            v = float(r["total_nilai"])
            agg[p]["total_trx"] += 1
            agg[p]["total_belanja"] += v
            agg[p]["maks_belanja"] = max(agg[p]["maks_belanja"], v)
            agg[p]["kategori"].add(r["kategori"])
        pelanggan_agregat = []
        for pid in sorted(agg.keys()):
            a = agg[pid]
            n = a["total_trx"]
            pelanggan_agregat.append({
                "id_pelanggan": pid,
                "total_trx": n,
                "total_belanja": round(a["total_belanja"], 2),
                "avg_belanja": round(a["total_belanja"] / n, 2),
                "maks_belanja": round(a["maks_belanja"], 2),
                "ragam_kategori": len(a["kategori"]),
            })
        self.write_json(out / "pelanggan_agregat.json", pelanggan_agregat)

    def _export_viz(self, module: str, n: int, n_p: int) -> tuple[list[dict], list[dict], dict]:
        partisipan = self.pipeline.generate_partisipan(n_p)
        aktivitas = self.pipeline.generate_aktivitas(n, partisipan)
        pid_idx = {p["id_partisipan"]: i + 1 for i, p in enumerate(partisipan)}

        silver = []
        for a in aktivitas:
            idx = pid_idx.get(a["id_partisipan"], 1)
            silver.append({
                "id_transaksi": a["id_aktivitas"].replace("ACT-", "")[:8],
                "id_pelanggan": f"usr-{idx:04d}",
                "kategori": a["kelas_layanan"],
                "channel": a["saluran"],
                "kota": a["unit_geografis"],
                "kuantitas": a["kuantitas"],
                "harga_satuan": a["harga_satuan"],
                "diskon": a["rasio_penyesuaian"],
                "total_nilai": a["nilai_total"],
                "tahun": a["tahun"],
                "bulan": a["bulan"],
                "tanggal": a["tanggal"],
                "tanggal_transaksi": a["tanggal"],
            })

        gold = self.pipeline.compute_gold(aktivitas, partisipan)
        out = self._module_dir(module)
        self.write_csv(out / "silver_transaksi.csv", silver, list(silver[0].keys()))
        for name, rows in gold.items():
            if rows:
                self.write_csv(out / f"gold_{name}.csv", rows, list(rows[0].keys()))
        tren_lanjutan = self.pipeline.compute_tren_lanjutan(gold["tren_bulanan"])
        if tren_lanjutan:
            self.write_csv(out / "gold_tren_lanjutan.csv", tren_lanjutan, list(tren_lanjutan[0].keys()))
        return aktivitas, partisipan, gold

    def export_ch04_hadoop(self) -> None:
        out = self._module_dir("ch04_hadoop")
        latihan = out / "latihan.txt"
        wordcount = out / "dataset_wordcount.txt"
        latihan.write_text("\n".join(CH04_LATIHAN_LINES) + "\n", encoding="utf-8")
        wordcount.write_text("\n".join(CH04_WORDCOUNT_LINES) + "\n", encoding="utf-8")

    def export_ch12_viz(self) -> None:
        cfg = self.schema["module_exports"]["ch12_viz"]
        self._export_viz("ch12_viz", cfg["n_rows"], cfg.get("n_partisipan", 300))

    def export_ch14_e2e(self) -> None:
        cfg = self.schema["module_exports"]["ch14_e2e"]
        inherit = cfg.get("inherits", "ch12_viz")
        base = self.schema["module_exports"][inherit]
        self._export_viz("ch14_e2e", base["n_rows"], base.get("n_partisipan", 300))

    def export_all(self) -> None:
        exporters = [
            self.export_ch03_minio,
            self.export_ch04_hadoop,
            self.export_ch05_spark,
            self.export_ch06_medallion,
            self.export_ch08_storage,
            self.export_ch09_orchestration,
            self.export_ch10_streaming,
            self.export_ch11_ml,
            self.export_ch12_viz,
            self.export_ch14_e2e,
        ]
        for fn in exporters:
            name = fn.__name__.replace("export_", "")
            print(f"[generate] {name} ...")
            fn()
            print(f"[OK] {name}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def load_schema(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Generator data sintesis Gaussian Copula")
    parser.add_argument(
        "--schema",
        type=Path,
        default=root / "config" / "schema_v1.yaml",
        help="Path ke schema YAML",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "outputs",
        help="Direktori output",
    )
    parser.add_argument(
        "--module",
        default="all",
        help="Modul target: all | ch03_minio | ch05_spark | ch06_medallion | ...",
    )
    parser.add_argument("--seed", type=int, default=None, help="Override random seed")
    args = parser.parse_args(argv)

    schema = load_schema(args.schema)
    seed = args.seed if args.seed is not None else schema.get("random_seed", 42)
    pipeline = SyntheticPipeline(schema, seed=seed)
    exporter = ModuleExporter(pipeline, args.output_dir)

    dispatch = {
        "ch03_minio": exporter.export_ch03_minio,
        "ch04_hadoop": exporter.export_ch04_hadoop,
        "ch05_spark": exporter.export_ch05_spark,
        "ch06_medallion": exporter.export_ch06_medallion,
        "ch07_medallion_local": exporter.export_ch06_medallion,
        "ch08_storage": exporter.export_ch08_storage,
        "ch09_orchestration": exporter.export_ch09_orchestration,
        "ch10_streaming": exporter.export_ch10_streaming,
        "ch11_ml": exporter.export_ch11_ml,
        "ch12_viz": exporter.export_ch12_viz,
        "ch14_e2e": exporter.export_ch14_e2e,
    }

    if args.module == "all":
        exporter.export_all()
    elif args.module in dispatch:
        print(f"[generate] {args.module} ...")
        dispatch[args.module]()
        print(f"[OK] {args.module}")
    else:
        parser.error(f"Modul tidak dikenal: {args.module}. Pilihan: all, {', '.join(dispatch)}")

    print(f"\nOutput ditulis ke: {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
