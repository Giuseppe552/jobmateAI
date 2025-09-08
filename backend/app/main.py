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

@api.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = str(uuid.uuid4())
    request_id_ctx.set(rid)
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    logger.info("request", request_id=rid, path=request.url.path, method=request.method, status_code=response.status_code)
    return response

@api.get("/health")
def health():
    return {"ok": True}

@api.post("/score")
def score(req: MatchRequest):
    result = score_pair(req.cv_text, req.jd_text)
    return result

@api.post("/rewrite")
def rewrite(req: MatchRequest):
    return {"bullets": make_bullets(req.cv_text, req.jd_text)}
