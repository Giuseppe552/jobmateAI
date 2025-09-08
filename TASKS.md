Tasks (Copilot – do in order)

Fill out utils: logging.py, config.py, rate_limit.py, cache.py.

Implement embeddings cache in services/embeddings.py using all-MiniLM-L6-v2.

Implement parser in services/parser.py with pdfplumber + text fallback.

Upgrade scorer in services/scorer.py:

Use embeddings cosine similarity.

Use TF-IDF to surface top overlapping n-grams as matches.

Derive gaps by JD keywords not in CV (normalized), cap at 10.

Wire rate limiting middleware in app/main.py (10 req/min/IP).

Write tests for scorer and API happy path + rate-limit failure.

Frontend: implement page.tsx UI and connect to API.

README: add live URLs, quickstart, API examples, screenshots placeholders.

Non-Goals

No databases.

No paid LLMs/APIs.

No auth (demo only).


### 2) Ensure root `render.yaml` (if it’s not at root, move it)
```yaml
services:
  - type: web
    name: jobmateai-api
    env: docker
    plan: free
    autoDeploy: true
    region: frankfurt
    rootDir: backend
    healthCheckPath: /health

3) Make sure CI is correct (.github/workflows/ci.yml)
name: CI
on: [push, pull_request]
jobs:
  backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: |
          echo "PYTHONPATH=$PWD" >> $GITHUB_ENV
          pytest -q

Exact Copilot Chat prompts you can paste (and where to run them)

Open Copilot Chat in VS Code. Use @workspace so it reads your repo. Run the prompts in the folder indicated.

A) Backend utilities (run from backend/app/utils/)

Prompt:

@workspace Create the following utility modules for a FastAPI app:
1) logging.py: structlog setup with JSON logs, include request_id, path, method, status_code. Provide get_logger().
2) config.py: pydantic-settings class AppSettings with fields: DEBUG(bool)=False, EMBEDDING_MODEL(str)="sentence-transformers/all-MiniLM-L6-v2", CACHE_DIR(str)=".cache", RATE_LIMIT_PER_MIN(int)=10. Provide load_settings() singleton.
3) rate_limit.py: simple in-memory token bucket by client IP, limit RATE_LIMIT_PER_MIN, FastAPI middleware class RateLimiterMiddleware.
4) cache.py: file-based cache: put(key:str, bytes), get(key:str)->Optional[bytes], using CACHE_DIR; key is sha256 of text when used by embeddings.
Write production-ready code with typing, docstrings, and safe dirs creation.

B) Embeddings with cache (run from backend/app/services/)

Prompt:

@workspace Implement embeddings.py that loads sentence-transformers model from settings.EMBEDDING_MODEL. 
- Provide get_embedding(text:str)->List[float] with LRU cache, and a batch version embed_many(texts:List[str])->List[List[float]].
- Persist embeddings on disk using utils.cache with sha256(text+model_name) as key.
- Handle model lazy-load and re-use across requests.
- Add graceful fallback if model is missing by raising HTTPException 500 with clear message.

C) Parser (PDF/text) (run from backend/app/services/)

Prompt:

@workspace Implement parser.py:
- function extract_text(file: UploadFile) -> str using pdfplumber for PDFs; else read bytes decode('utf-8','ignore').
- function normalize_text(s:str) -> str: collapse whitespace, normalize unicode, lower-case only for keyword ops.
- Include a helper to split into sections (skills/experience/education) with simple regex headings; safe if absent.
Add tests stub-friendly design.

D) Scorer (explainable) (run from backend/app/services/)

Prompt:

@workspace Implement scorer.py to return:
{
  "score": float,                # 0..1 cosine similarity of mean pooled embeddings
  "matches": List[str],          # top 10 overlapping n-grams (1-2) by TF-IDF product
  "gaps": List[str],             # up to 10 JD keywords not present in CV
  "weights": {"skills":0.5,"responsibilities":0.3,"tools":0.2}
}
- Use services.embeddings to embed texts (mean of tokens).
- Use TfidfVectorizer(ngram_range=(1,2), stop_words='english') for matches.
- For gaps: tokenize JD, remove stopwords, remove words length<4, subtract CV set, take most frequent.
- Provide function score_pair(cv_text:str, jd_text:str)->Dict.
- Pure functions, typed, deterministic.

E) Rewrite (deterministic) (run from backend/app/services/)

Prompt:

@workspace Implement rewrite.py:
- make_bullets(cv_text:str, jd_text:str)->List[str]
- Extract top 5 verbs/nouns from JD and produce 5 bullet templates in STAR/CAR style with placeholders quantified.
- Deterministic output, no randomness or external APIs.

F) Wire middleware + routes (run from backend/app/main.py)

Prompt:

@workspace Update main.py:
- Add RateLimiterMiddleware to api with limit from settings.
- Add request_id per request (uuid4) in contextvar and include in logs.
- Ensure /health, /score, /rewrite endpoints use models.MatchRequest and return JSON serializable dicts.
- Add CORS allow all for demo.

G) Tests (run from backend/tests/)

Prompt:

@workspace Create pytest tests:
1) test_api.py: /health returns ok; /score with simple strings returns score in [0,1] and lists; rate limiting returns 429 on >limit rapid calls (mock limit low).
2) test_scorer.py: known CV/JD pair yields higher score than unrelated pair; matches non-empty for overlapping terms; gaps non-empty when JD has unique keywords.
Use FastAPI TestClient.

H) Frontend (run from frontend/)

Prompt:

@workspace Implement src/app/page.tsx for Next.js App Router:
- Two textareas (CV, JD), a submit button.
- POST to `${process.env.NEXT_PUBLIC_API_URL}/score` with JSON body.
- Render score, matches, gaps. Loading/error states. Simple Tailwind styling.
- No server actions; client component only.

Sanity checks you must run (you, not Copilot)
# Backend local test
cd backend
pip install -r requirements.txt
pytest -q
uvicorn app.main:api --reload
# visit http://127.0.0.1:8000/health

# Commit and push, ensure CI goes green
git add -A
git commit -m "feat: utils+services implemented; rate limit; tests added"
git push origin main


Render deploy:

Render → New → Blueprint → select repo.

Confirm it reads root render.yaml and uses backend as rootDir.

After deploy, hit /health.

Vercel:

Set NEXT_PUBLIC_API_URL to your Render URL.

Deploy frontend.

Your assignment (no excuses)

Create TASKS.md and paste it exactly.

Run the Copilot prompts A–G in order.

Get CI green.

Deploy the backend (Blueprint detects render.yaml at root).

Drop the live /health URL here.
