"""Generator 500 transaksi + 50 pelanggan (seed=42)."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

from paths import DATA_DIR

random.seed(42)
KATEGORI = ["Elektronik", "Fashion", "Kuliner", "Kesehatan", "Olahraga"]
KOTA = ["Jakarta", "Bandung", "Surabaya", "Medan", "Makassar"]
SEGMEN = ["Premium", "Regular", "Basic"]


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    trx_path = DATA_DIR / "transaksi.csv"
    plg_path = DATA_DIR / "pelanggan.csv"

    with trx_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            ["id_transaksi", "id_pelanggan", "tanggal", "kategori", "total_nilai", "kota"]
        )
        for i in range(1, 501):
            tgl = date(2024, 1, 1) + timedelta(days=random.randint(0, 364))
            w.writerow(
                [
                    f"TRX-{i:05d}",
                    f"PLG-{random.randint(1, 50):04d}",
                    tgl.isoformat(),
                    random.choice(KATEGORI),
                    round(random.uniform(50000, 5000000), 2),
                    random.choice(KOTA),
                ]
            )

    with plg_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id_pelanggan", "nama", "segmen", "kota_asal"])
        for i in range(1, 51):
            w.writerow(
                [
                    f"PLG-{i:04d}",
                    f"Pelanggan-{i:04d}",
                    random.choice(SEGMEN),
                    random.choice(KOTA),
                ]
            )

    print(f"[OK] {trx_path} ({trx_path.stat().st_size} byte)")
    print(f"[OK] {plg_path} ({plg_path.stat().st_size} byte)")


if __name__ == "__main__":
    main()
