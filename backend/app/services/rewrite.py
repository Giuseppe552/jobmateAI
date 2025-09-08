from typing import List
import re
from collections import Counter

def make_bullets(cv_text: str, jd_text: str) -> List[str]:
    # Extract top 5 verbs/nouns from JD
    tokens = re.findall(r"\w+", jd_text.lower())
    words = [w for w in tokens if len(w) > 3]
    freq = Counter(words)
    top = [w for w, _ in freq.most_common(10)]
    verbs = [w for w in top if re.match(r"\b\w+ing\b", w) or w.endswith('ed')]
    nouns = [w for w in top if w not in verbs]
    selected = (verbs[:3] + nouns[:2])[:5]
    # STAR/CAR templates
    templates = [
        f"Situation: Describe a time you {{verb}} using {{noun}} to achieve a result.",
        f"Task: Explain how you handled {{verb}} responsibilities with {{noun}}.",
        f"Action: Detail steps taken to {{verb}} leveraging {{noun}}.",
        f"Result: Quantify the impact of your {{verb}} on {{noun}} outcomes.",
        f"Challenge: Share how you overcame obstacles while {{verb}} with {{noun}}."
    ]
    bullets = [t.replace("{{verb}}", selected[i%len(selected)]).replace("{{noun}}", selected[(i+1)%len(selected)]) for i, t in enumerate(templates)]
    return bullets
