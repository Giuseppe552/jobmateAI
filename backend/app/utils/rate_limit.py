"""
Simple in-memory token bucket rate limiter by client IP.
FastAPI middleware RateLimiterMiddleware.
"""
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict
import time

class TokenBucket:
    def __init__(self, rate: int, per: int = 60):
        self.rate = rate
        self.per = per
        self.tokens: Dict[str, float] = {}
        self.timestamps: Dict[str, float] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        tokens = self.tokens.get(key, self.rate)
        last = self.timestamps.get(key, now)
        elapsed = now - last
        tokens = min(self.rate, tokens + elapsed * (self.rate / self.per))
        if tokens >= 1:
            tokens -= 1
            self.tokens[key] = tokens
            self.timestamps[key] = now
            return True
        self.tokens[key] = tokens
        self.timestamps[key] = now
        return False

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate: int):
        super().__init__(app)
        self.bucket = TokenBucket(rate)

    async def dispatch(self, request: Request, call_next):
        # Always allow /health endpoint
        if request.url.path == "/health":
            return await call_next(request)
        ip = request.client.host
        if not self.bucket.allow(ip):
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        response = await call_next(request)
        return response
