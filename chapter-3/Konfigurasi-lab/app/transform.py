"""Transformasi Bronze -> Silver: dedup, imputasi, standarisasi, Parquet."""
from io import BytesIO, StringIO

import pandas as pd

from s3_client import get_s3_client

BRONZE_KEY = "users/sample_users.csv"
SILVER_KEY = "users/users_clean.parquet"


def main():
    s3 = get_s3_client()

    response = s3.get_object(Bucket="bronze", Key=BRONZE_KEY)
    df = pd.read_csv(StringIO(response["Body"].read().decode("utf-8")))
    print(f"Bronze: {len(df)} baris, {df.shape[1]} kolom")

    df = df.drop_duplicates()
    df["salary"] = df["salary"].fillna(df["salary"].median())
    df.columns = df.columns.str.lower().str.strip()
    df["join_date"] = pd.to_datetime(df["join_date"])
    df["salary"] = df["salary"].astype(float)
    df["processed_at"] = pd.Timestamp.now()
    df["source"] = f"bronze/{BRONZE_KEY}"
    print(f"Silver: {len(df)} baris setelah transformasi")

    buffer = BytesIO()
    df.to_parquet(buffer, index=False, engine="pyarrow")
    buffer.seek(0)
    s3.put_object(Bucket="silver", Key=SILVER_KEY, Body=buffer.getvalue())
    print("Selesai: Data bersih tersimpan di Silver layer")
    print(f"Key: silver/{SILVER_KEY}")


if __name__ == "__main__":
    main()
