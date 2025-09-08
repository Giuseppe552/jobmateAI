from __future__ import annotations
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def _tfidf(a: str, b: str) -> Tuple[float, List[str]]:
    vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    X = vec.fit_transform([a, b])
    score = float(cosine_similarity(X[0], X[1])[0][0])
    contrib = (X[0].multiply(X[1])).toarray()[0]
    items = sorted(zip(vec.get_feature_names_out(), contrib), key=lambda x: x[1], reverse=True)
    matches = [t for t, w in items[:10] if w > 0]
    return score, matches

_STOP = {"and","the","for","with","you","your","our","are","will","have","has","this","that","from","into","work","team","role","job","skills","experience","years","ability","required","preferred"}
_WORD = re.compile(r"[A-Za-z][A-Za-z0-9\-\+\.]{3,}")

def _gaps(cv: str, jd: str, k: int = 10) -> List[str]:
    jd_tokens = [w.lower() for w in _WORD.findall(jd)]
    cv_set = set(w.lower() for w in _WORD.findall(cv))
    seen, out = set(), []
    for w in jd_tokens:
        if w not in _STOP and w not in cv_set and w not in seen:
            out.append(w); seen.add(w)
            if len(out) >= k: break
    return out

def score_pair(cv: str, jd: str) -> Dict:
    score, matches = _tfidf(cv, jd)
    return {
        "score": round(max(0.0, min(1.0, score)), 4),
        "matches": matches,
        "gaps": _gaps(cv, jd, 10),
        "weights": {"skills": 0.5, "responsibilities": 0.3, "tools": 0.2},
    }

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
