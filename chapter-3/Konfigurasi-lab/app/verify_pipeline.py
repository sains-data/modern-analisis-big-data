"""Verifikasi object wajib di Bronze, Silver, dan Gold."""
from botocore.exceptions import ClientError

from s3_client import get_s3_client

REQUIRED = {
    "bronze": ["users/sample_users.csv"],
    "silver": ["users/users_clean.parquet"],
    "gold": ["summary/city_summary.parquet"],
}


def object_exists(s3, bucket: str, key: str) -> bool:
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError:
        return False


def main():
    s3 = get_s3_client()
    ok = True

    print("=== Verifikasi pipeline Medallion ===\n")
    for bucket, keys in REQUIRED.items():
        print(f"[{bucket.upper()}]")
        for key in keys:
            exists = object_exists(s3, bucket, key)
            status = "OK" if exists else "MISSING"
            print(f"  {status:7} {bucket}/{key}")
            ok = ok and exists
        print()

    if ok:
        print("Semua object wajib ditemukan.")
    else:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
