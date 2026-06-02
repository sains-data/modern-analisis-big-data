# Selaras Data-Lakehouse-Metadata: Python 3.10 + provider Spark/Hive
FROM apache/airflow:2.9.1-python3.10

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-jre-headless curl docker.io \
    && rm -rf /var/lib/apt/lists/*

USER airflow
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark==4.8.1 \
    apache-airflow-providers-apache-hive==6.4.2 \
    requests==2.31.0 \
    pyspark==3.5.5
