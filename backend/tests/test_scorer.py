from app.services.scorer import score_pair

def test_score_pair_similarity():
    cv = "Python AWS pandas"
    jd = "Python AWS pandas"
    unrelated = "Banana Apple Orange"
    s1 = score_pair(cv, jd)["score"]
    s2 = score_pair(cv, unrelated)["score"]
    assert s1 > s2

def test_score_pair_matches_gaps():
    cv = "Python pandas AWS"
    jd = "Python AWS experience cloud"
    out = score_pair(cv, jd)
    assert len(out["matches"]) > 0
    assert len(out["gaps"]) > 0  # 'cloud' should be a gap
