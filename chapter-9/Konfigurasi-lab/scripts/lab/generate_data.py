#!/usr/bin/env python3
"""
generate_data.py — Generator data transaksi sintetis untuk Modul 7
Penggunaan: python generate_data.py <tanggal YYYY-MM-DD> <jumlah_baris>
Output    : CSV ke stdout dengan header id,nilai,kategori
"""

import sys
import random
import uuid


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_data.py <tanggal> <jumlah_baris>", file=sys.stderr)
        sys.exit(1)

    tanggal = sys.argv[1]
    n = int(sys.argv[2])

    random.seed(hash(tanggal) % (2**31))

    KATEGORI = ["elektronik", "fashion", "makanan", "kesehatan", "otomotif"]
    HARGA_BASE = {
        "elektronik": 500_000,
        "fashion": 200_000,
        "makanan": 50_000,
        "kesehatan": 150_000,
        "otomotif": 800_000,
    }

    print("id,nilai,kategori")

    for _ in range(1, n + 1):
        kat = random.choice(KATEGORI)
        nilai = int(HARGA_BASE[kat] * random.uniform(0.5, 3.0))
        tid = f"T{str(uuid.uuid4())[:6].upper()}"

        if random.random() < 0.03:
            if random.random() < 0.5:
                tid = ""
            else:
                nilai = -nilai

        print(f"{tid},{nilai},{kat}")


if __name__ == "__main__":
    main()
