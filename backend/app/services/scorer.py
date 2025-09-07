from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _top_terms(a: str, b: str, k: int = 10) -> List[str]:
    vec = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
    X = vec.fit_transform([a, b])
    v = (X[0].multiply(X[1])).toarray()[0]
    items = sorted(zip(vec.get_feature_names_out(), v), key=lambda x: x[1], reverse=True)
    return [t for t, w in items[:k] if w > 0]

def score_pair(cv: str, jd: str) -> Dict:
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform([cv, jd])
    score = float(cosine_similarity(X[0], X[1])[0][0])
    return {
        "score": round(score, 4),
        "matches": _top_terms(cv, jd, 10),
        "gaps": _infer_gaps(cv, jd, 10),
        "weights": {"skills": 0.5, "responsibilities": 0.3, "tools": 0.2},  # placeholder for UI
    }

def _infer_gaps(cv: str, jd: str, k: int = 10) -> List[str]:
    jd_terms = set(t.lower() for t in jd.split())
    cv_terms = set(t.lower() for t in cv.split())
    missing = [t for t in jd_terms - cv_terms if t.isalpha() and len(t) > 3]
    return missing[:k]
