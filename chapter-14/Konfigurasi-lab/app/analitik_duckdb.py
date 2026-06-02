"""Analitik gaya Trino dengan DuckDB — Bab 14 Tahap 2."""
from pathlib import Path

import duckdb

LAB_ROOT = Path(__file__).resolve().parent.parent
GOLD = LAB_ROOT / "data" / "gold"


def main() -> None:
    con = duckdb.connect()

    con.execute(
        f"""
        CREATE OR REPLACE VIEW tren_bulanan AS
        SELECT * FROM read_parquet('{GOLD}/tren_bulanan/**/*.parquet');
        """
    )
    con.execute(
        f"""
        CREATE OR REPLACE VIEW omzet_kategori AS
        SELECT * FROM read_parquet('{GOLD}/omzet_kategori/**/*.parquet');
        """
    )
    con.execute(
        f"""
        CREATE OR REPLACE VIEW segmentasi_rfm AS
        SELECT * FROM read_parquet('{GOLD}/segmentasi_rfm/**/*.parquet');
        """
    )

    print("=== Tren Bulanan + MoM Growth ===")
    print(
        con.execute(
            """
            SELECT
                periode,
                ROUND(omzet/1e6, 2)     AS omzet_juta,
                n_transaksi,
                ROUND(ma3_omzet/1e6, 2) AS ma3_juta,
                mom_growth               AS mom_pct
            FROM tren_bulanan
            ORDER BY periode
            """
        ).df().to_string(index=False)
    )

    print("\n=== Omzet Kumulatif dan Ranking Kategori ===")
    print(
        con.execute(
            """
            SELECT
                kategori,
                ROUND(omzet_total/1e6, 2)             AS omzet_juta,
                persen_omzet,
                RANK() OVER (ORDER BY omzet_total DESC) AS peringkat,
                ROUND(
                    SUM(omzet_total) OVER (
                        ORDER BY omzet_total DESC
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) / SUM(omzet_total) OVER () * 100, 2
                ) AS kumulatif_pct
            FROM omzet_kategori
            ORDER BY omzet_total DESC
            """
        ).df().to_string(index=False)
    )

    print("\n=== Profil Segmen Pelanggan (RFM) ===")
    print(
        con.execute(
            """
            SELECT
                segmen_rfm,
                COUNT(*) AS n_pelanggan,
                ROUND(AVG(frekuensi), 1)     AS avg_frekuensi,
                ROUND(AVG(monetary)/1e3, 0)  AS avg_monetary_ribu,
                ROUND(AVG(recency_hari), 0)  AS avg_recency_hari
            FROM segmentasi_rfm
            GROUP BY segmen_rfm
            ORDER BY avg_monetary_ribu DESC
            """
        ).df().to_string(index=False)
    )

    print("\n=== Analisis Growth Rate ===")
    print(
        con.execute(
            """
            SELECT
                periode,
                ROUND(omzet/1e6, 2) AS omzet_juta,
                mom_growth,
                CASE
                    WHEN mom_growth > 15 THEN 'Tinggi'
                    WHEN mom_growth < 0  THEN 'Kontraksi'
                    ELSE 'Normal'
                END AS status_growth
            FROM tren_bulanan
            WHERE mom_growth IS NOT NULL
            ORDER BY mom_growth DESC
            """
        ).df().to_string(index=False)
    )

    con.close()
    print("\n[OK] Analitik DuckDB selesai")


if __name__ == "__main__":
    main()
