
 <img src="screenshot.png" alt="JobMateAI demo image" width="80%">

# JobMateAI

[![CI](https://github.com/Giuseppe552/jobmateAI/actions/workflows/ci.yml/badge.svg)](https://github.com/Giuseppe552/jobmateAI/actions/workflows/ci.yml)
[![Render Deploy](https://img.shields.io/badge/Backend-Render-blue?logo=render)](https://render.com/)
[![Vercel Deploy](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](https://vercel.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?logo=python)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com/)

---

👉 **Live Demo:**  
- Frontend: [jobmate-ai.vercel.app](https://jobmate-ai-six.vercel.app/)
- Backend: [jobmateai-api.onrender.com/health](https://jobmateai-api.onrender.com/health)


> **JobMateAI** is a modern, explainable AI platform for matching CVs to job descriptions, built for recruiters and candidates. Designed for speed, transparency, and demo simplicity—no databases, no paid APIs, no authentication.

---

## 🏁 Quickstart
 
### Backend (FastAPI)
```bash
git clone https://github.com/Giuseppe552/jobmateAI.git
cd jobmateAI/backend
pip install -r requirements.txt
pytest -q
uvicorn app.main:api --reload
# Visit: http://127.0.0.1:8000/health
```

### Frontend (Next.js)
```bash
cd ../frontend
npm install
# Set API URL in .env.local
echo NEXT_PUBLIC_API_URL=[your Render backend URL] > .env.local
npm run dev
# Visit: http://localhost:3000
```

---

## 🧠 Features

- **Explainable Scoring:** Cosine similarity, TF-IDF n-gram matches, and gap analysis.
- **Embeddings Cache:** Fast, file-based, using MiniLM-L6-v2.
- **PDF/Text Parsing:** Robust extraction and normalization.
- **Deterministic Rewrite:** STAR/CAR bullet suggestions, no external APIs.
- **Rate Limiting:** Demo-safe, per-IP.
- **Modern UI:** Next.js + Tailwind, instant feedback.

---

## 📦 API Examples

**POST /score**
```json
{
  "cv_text": "Python developer with AWS experience",
  "jd_text": "Looking for Python and AWS skills"
}
```
Response:
```json
{
  "score": 0.87,
  "matches": ["python", "aws"],
  "gaps": ["cloud"],
  "weights": {"skills":0.5,"responsibilities":0.3,"tools":0.2}
}
```

**POST /rewrite**
```json
{
  "cv_text": "...",
  "jd_text": "..."
}
```
Response:
```json
{
  "bullets": ["Situation: ...", "Task: ...", ...]
}
```

---

## 📸 Screenshots

*Add screenshots here to showcase the UI and API responses.*

---

## 🛠️ Deployment

- **Backend:** Render (auto-detects `render.yaml` at repo root)
- **Frontend:** Vercel (set `NEXT_PUBLIC_API_URL` to backend URL)

---

## ❌ Non-Goals

- No databases
- No paid LLMs/APIs
- No authentication (demo only)

---

## 📬 Contact

For questions, feedback, or collaboration, reach out via [GitHub Issues](https://github.com/Giuseppe552/jobmateAI/issues).

Or email: contact.giuseppe00@gmail.com
