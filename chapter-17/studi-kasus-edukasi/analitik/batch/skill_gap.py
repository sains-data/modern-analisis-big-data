#!/usr/bin/env python3
"""NLP skill gap — TF-IDF lowongan vs kurikulum CPL."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from analitik.lib.config import BRONZE, GOLD, SKILL_GAP_MIN

GOLD.mkdir(parents=True, exist_ok=True)

STOP = {"dan", "atau", "the", "with", "for", "in", "of", "a", "to", "yang", "pada", "dengan"}


def top_terms(texts: list[str], top_n: int = 30) -> set[str]:
    vec = TfidfVectorizer(max_features=top_n, stop_words=list(STOP), token_pattern=r"[a-zA-Z]{3,}")
    mat = vec.fit_transform(texts)
    return set(vec.get_feature_names_out())


def main() -> None:
    jobs = pd.read_parquet(BRONZE / "lowongan_kerja.parquet")
    kur = pd.read_parquet(BRONZE / "kurikulum.parquet")

    job_terms = top_terms(jobs["deskripsi"].tolist(), 40)
    kur_terms = top_terms(kur["deskripsi_cpl"].tolist(), 40)
    gap_terms = sorted(job_terms - kur_terms)

    rows = []
    kur_vec = TfidfVectorizer(stop_words=list(STOP), token_pattern=r"[a-zA-Z]{3,}")
    kur_mat = kur_vec.fit_transform(kur["deskripsi_cpl"])
    kur_names = kur_vec.get_feature_names_out()

    for term in gap_terms[: max(SKILL_GAP_MIN, 15)]:
        if term not in kur_names:
            mk_rek = kur.iloc[0]["kode_mk"]
            score = 0.0
        else:
            idx = list(kur_names).index(term)
            scores = kur_mat[:, idx].toarray().ravel()
            best = int(scores.argmax())
            mk_rek = kur.iloc[best]["kode_mk"]
            score = float(scores[best])
        freq = jobs["deskripsi"].str.lower().str.contains(term.lower()).mean() * 100
        rows.append(
            {
                "skill": term,
                "frekuensi_pct": round(freq, 1),
                "matkul_rekomendasi": mk_rek,
                "cosine_relevansi": round(score, 3),
            }
        )

    df = pd.DataFrame(rows).sort_values("frekuensi_pct", ascending=False)
    df.to_parquet(GOLD / "skill_gap_kurikulum.parquet", index=False)
    df.head(10).to_parquet(GOLD / "rekomendasi_kurikulum.parquet", index=False)
    print(f"[OK] skill_gap {len(df)} skill (min {SKILL_GAP_MIN})")


if __name__ == "__main__":
    main()
