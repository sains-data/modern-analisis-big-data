"""Upload data mentah ke bucket Bronze (tanpa transformasi)."""
from pathlib import Path

from s3_client import get_s3_client

BRONZE_KEY = "users/sample_users.csv"
LOCAL_FILE = Path("/raw-data/sample_users.csv")


def main():
    if not LOCAL_FILE.is_file():
        raise FileNotFoundError(f"File tidak ditemukan: {LOCAL_FILE}")

    s3 = get_s3_client()
    s3.upload_file(str(LOCAL_FILE), "bronze", BRONZE_KEY)
    print("Berhasil: Data mentah tersimpan di Bronze layer")
    print(f"Key: bronze/{BRONZE_KEY}")


if __name__ == "__main__":
    main()
