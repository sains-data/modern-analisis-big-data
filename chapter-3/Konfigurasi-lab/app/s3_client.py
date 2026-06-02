"""Klien S3/MinIO bersama untuk skrip latihan Chapter 3."""
import os

import boto3


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.environ.get("MINIO_ENDPOINT", "http://minio:9000"),
        aws_access_key_id=os.environ.get("MINIO_ACCESS_KEY", "admin"),
        aws_secret_access_key=os.environ.get("MINIO_SECRET_KEY", "admin123"),
    )
