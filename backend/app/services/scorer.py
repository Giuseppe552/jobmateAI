"""
Scorer service for CV/JD matching with explainable output.
Cosine similarity of mean pooled embeddings, TF-IDF n-gram matches, JD gaps.
"""
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import numpy as np
import re
from .embeddings import get_embedding

WEIGHTS = {"skills": 0.5, "responsibilities": 0.3, "tools": 0.2}

STOPWORDS = set(TfidfVectorizer(stop_words='english').get_stop_words())

def mean_pool(emb: List[float]) -> np.ndarray:
    return np.array(emb)

def score_pair(cv_text: str, jd_text: str) -> Dict:
    cv_emb = mean_pool(get_embedding(cv_text))
    jd_emb = mean_pool(get_embedding(jd_text))
    score = float(cosine_similarity([cv_emb], [jd_emb])[0][0])

    try:
        vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words='english')
        tfidf = vectorizer.fit_transform([cv_text, jd_text])
        jd_ngrams = vectorizer.get_feature_names_out()
        jd_vec = tfidf[1].toarray()[0]
        cv_vec = tfidf[0].toarray()[0]
        products = jd_vec * cv_vec
        top_idx = np.argsort(products)[::-1][:10]
        matches = [jd_ngrams[i] for i in top_idx if products[i] > 0]
    except ValueError:
        matches = []

    # Gaps: JD keywords not in CV
    jd_tokens = [w for w in re.findall(r"\w+", jd_text.lower()) if w not in STOPWORDS and len(w) >= 4]
    cv_tokens = set(re.findall(r"\w+", cv_text.lower()))
    gaps = [w for w, _ in Counter(jd_tokens).most_common() if w not in cv_tokens][:10]

    return {
        "score": score,
        "matches": matches,
        "gaps": gaps,
        "weights": WEIGHTS
    }

def _infer_gaps(cv: str, jd: str, k: int = 10) -> List[str]:
    jd_terms = set(t.lower() for t in jd.split())
    cv_terms = set(t.lower() for t in cv.split())
    missing = [t for t in jd_terms - cv_terms if t.isalpha() and len(t) > 3]
    return missing[:k]
