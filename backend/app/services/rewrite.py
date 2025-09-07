from typing import List

def make_bullets(cv: str, jd: str) -> List[str]:
    # deterministic, template-based (no paid LLMs)
    verbs = ["Led","Built","Automated","Optimized","Deployed","Reduced","Improved"]
    keywords = list({w for w in jd.split() if w.istitle()})[:5]
    base = [
        f"{verbs[i%len(verbs)]} {kw} initiatives aligned to role requirements; quantified impact where possible."
        for i, kw in enumerate(keywords)
    ]
    return base or ["Tailor bullets to JD keywords; quantify outcome with %/time/$."]
