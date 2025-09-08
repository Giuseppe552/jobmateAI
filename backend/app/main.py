from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.scorer import score_pair

app = FastAPI(title="JobMate AI", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchRequest(BaseModel):
    cv_text: str
    jd_text: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/score")
def score(req: MatchRequest):
    try:
        return score_pair(req.cv_text, req.jd_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"scoring_failed: {type(e).__name__}: {e}")
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.models import MatchRequest
from app.services.scorer import score_pair
from app.services.rewrite import make_bullets
from app.utils.config import load_settings
from app.utils.rate_limit import RateLimiterMiddleware
from app.utils.logging import setup_logging, get_logger
import uuid
import contextvars

setup_logging()
logger = get_logger()
request_id_ctx = contextvars.ContextVar("request_id", default=None)


api = FastAPI(title="JobMate AI", version="2.0")
settings = load_settings()
api.add_middleware(RateLimiterMiddleware, rate=settings.RATE_LIMIT_PER_MIN)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/")
def root():
    return {
        "message": "🚀 JobMateAI: The open-source, explainable CV-to-JD matcher. Built for recruiters, candidates, and hackers. See /health, /score, /rewrite endpoints."
    }

