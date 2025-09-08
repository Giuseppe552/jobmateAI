# JobMateAI

[![CI](https://github.com/Giuseppe552/jobmateAI/actions/workflows/ci.yml/badge.svg)](https://github.com/Giuseppe552/jobmateAI/actions/workflows/ci.yml)
[![Backend](https://img.shields.io/badge/Backend-Render-blue?logo=render)](https://render.com/)
[![Frontend](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](https://vercel.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?logo=python)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=nextdotjs)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com/)

---

👉 **Live Demo**  
- Frontend: [jobmate-ai.vercel.app](https://jobmate-ai.vercel.app)  
- Backend: [jobmateai-api.onrender.com/health](https://jobmateai-api.onrender.com/health)

---

## 🚀 Overview

**JobMateAI** is a lightweight, explainable AI tool for matching CVs to job descriptions.  
It’s designed for recruiters and job seekers who want quick, transparent insights — without databases, paid APIs, or complex setup.  

Built as a **portfolio-ready full-stack project**:  
- **Frontend:** Next.js + Tailwind (Vercel deploy)  
- **Backend:** FastAPI (Render deploy)  
- **Scoring:** TF-IDF + cosine similarity for matches/gaps  

---

## 🏁 Quickstart

### Backend (FastAPI)

```bash
git clone https://github.com/Giuseppe552/jobmateAI.git
cd jobmateAI/backend
pip install -r requirements.txt

# run tests
pytest -q

# start API
uvicorn app.main:api --reload
# → http://127.0.0.1:8000/health
````

### Frontend (Next.js)

```bash
cd ../frontend
npm install

# set API base URL
echo NEXT_PUBLIC_API_URL=http://127.0.0.1:8000 > .env.local

# start dev server
npm run dev
# → http://localhost:3000
```

---

## 🧠 Features

* **Explainable Scoring:** Cosine similarity on TF-IDF n-grams
* **Gap Analysis:** Extract missing keywords from job description
* **Clean UI:** Next.js + Tailwind for recruiter/demo usability
* **No External Costs:** No paid APIs, no databases, no auth

---

## 📦 API Usage

**POST `/score`**

Request:

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
  "weights": {"skills": 0.5, "responsibilities": 0.3, "tools": 0.2}
}
```

---

## 📸 Screenshots

![Frontend demo](screenshot.png)

---

## 🛠️ Deployment

* **Backend:** Render (`render.yaml` auto-detected)
* **Frontend:** Vercel (`NEXT_PUBLIC_API_URL` → backend URL)

Both free-tier friendly. Cold starts may add a short delay.

---

## 🎯 Why this project

* Shows **end-to-end skills**: NLP, FastAPI, Docker, CI/CD, Next.js
* Built to be **cloned & reused** as a learning project
* Demonstrates **practical app for real problems** (ATS screening)

---

## 📬 Contact

* GitHub: [@Giuseppe552](https://github.com/Giuseppe552)
* LinkedIn: [Giuseppe](https://www.linkedin.com/in/Giuseppe552)
* Email: [contact.giuseppe00@gmail.com](mailto:contact.giuseppe00@gmail.com)

```

