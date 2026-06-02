"""Agregasi Silver -> Gold: ringkasan per kota."""
from io import BytesIO

import pandas as pd

from s3_client import get_s3_client

SILVER_KEY = "users/users_clean.parquet"
GOLD_KEY = "summary/city_summary.parquet"


def main():
    s3 = get_s3_client()

    response = s3.get_object(Bucket="silver", Key=SILVER_KEY)
    df = pd.read_parquet(BytesIO(response["Body"].read()))

    df_gold = (
        df.groupby("city")
        .agg(
            avg_salary=("salary", "mean"),
            total_karyawan=("id", "count"),
            avg_usia=("age", "mean"),
        )
        .reset_index()
        .round(2)
    )
    df_gold["generated_at"] = pd.Timestamp.now()
    print(df_gold.to_string(index=False))

    buffer = BytesIO()
    df_gold.to_parquet(buffer, index=False)
    buffer.seek(0)
    s3.put_object(Bucket="gold", Key=GOLD_KEY, Body=buffer.getvalue())
    print("Selesai: Data analitik tersimpan di Gold layer")
    print(f"Key: gold/{GOLD_KEY}")


if __name__ == "__main__":
    main()
