#!/usr/bin/env python3
"""Lowongan kerja industri — korpus NLP skill gap."""
import random
from pathlib import Path

import pandas as pd

random.seed(66)
CASE_ROOT = Path(__file__).resolve().parents[2]
OUT = CASE_ROOT / "data" / "sumber" / "karir" / "lowongan"
OUT.mkdir(parents=True, exist_ok=True)

SKILLS = [
    "python machine learning deep learning tensorflow pytorch data science",
    "cloud aws azure gcp kubernetes docker devops ci cd",
    "big data spark kafka hadoop airflow etl pipeline",
    "sql postgresql mongodb database warehouse lakehouse",
    "cybersecurity penetration testing siem encryption",
    "react nodejs javascript typescript fullstack web",
    "nlp natural language processing transformer bert llm",
    "mlops model deployment monitoring drift retraining",
    "computer vision opencv image classification yolo",
    "agile scrum product owner stakeholder management",
    "power bi tableau dashboard visualization analytics",
    "java spring boot microservices api rest graphql",
    "blockchain smart contract solidity web3",
    "iot edge computing mqtt sensor streaming",
    "android kotlin mobile flutter cross platform",
]

TITLES = [
    "Data Engineer", "ML Engineer", "Backend Developer", "DevOps Engineer",
    "Data Analyst", "Cloud Architect", "Full Stack Developer", "AI Researcher",
]


def main() -> None:
    rows = []
    for i in range(120):
        rows.append(
            {
                "lowongan_id": f"JOB{i+1:04d}",
                "judul": random.choice(TITLES),
                "deskripsi": random.choice(SKILLS) + " " + random.choice(SKILLS),
                "lokasi": random.choice(["Medan", "Jakarta", "Remote"]),
            }
        )
    pd.DataFrame(rows).to_csv(OUT / "lowongan_kerja.csv", index=False)
    print(f"[OK] lowongan_kerja.csv ({len(rows)} postingan)")


if __name__ == "__main__":
    main()
