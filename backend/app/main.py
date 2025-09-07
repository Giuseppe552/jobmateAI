from fastapi import FastAPI
from app.models import MatchRequest
from app.services.scorer import score_pair
from app.services.rewrite import make_bullets

api = FastAPI(title="JobMate AI", version="2.0")

@api.get("/health")
def health(): return {"ok": True}

@api.post("/score")
def score(req: MatchRequest):
    return score_pair(req.cv_text, req.jd_text)

@api.post("/rewrite")
def rewrite(req: MatchRequest):
    return {"bullets": make_bullets(req.cv_text, req.jd_text)}
