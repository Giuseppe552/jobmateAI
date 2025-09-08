"use client";
import { useState } from "react";
import axios from "axios";
// PDF parsing in browser is limited; fallback to manual paste

const API = process.env.NEXT_PUBLIC_API_URL!; // set on Vercel

export default function Home() {
  const [cv, setCv] = useState("");
  const [cvFileName, setCvFileName] = useState<string | null>(null);
  const [jd, setJd] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const [err, setErr] = useState<string|null>(null);
  const [res, setRes] = useState<any>(null);

  async function warmup(): Promise<void> {
    try {
      await axios.get(`${API}/health`, { timeout: 70000 });
    } catch { /* ignore */ }
  }

  async function analyze() {
    if (!cv.trim() || !jd.trim()) return;
    setLoading(true); setErr(null); setRes(null);
    try {
      if (!API) throw new Error("NEXT_PUBLIC_API_URL is not set");
      await warmup();
      const attempt = () => axios.post(
        `${API}/score`,
        { cv_text: cv, jd_text: jd },
        { timeout: 70000 }
      );
      let r;
      try { r = await attempt(); }
      catch { await new Promise(res => setTimeout(res, 1200)); r = await attempt(); }
      setRes(r.data);
    } catch (e: any) {
      const status = e?.response?.status;
      const detail = e?.response?.data?.detail;
      setErr(status ? `HTTP ${status} — ${detail || "Backend error"}` : (e?.message || "Network Error"));
    } finally {
      setLoading(false);
    }
  }

  function handleCVUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setCvFileName(file.name);
    setCv("PDF parsing is not supported in browser demo. Please paste CV text manually.");
  }

  return (
    <main className="min-h-screen w-full flex flex-col items-center justify-center bg-gradient-to-br from-blue-100 via-white to-blue-200 px-4 py-8">
      <div className="flex flex-col items-center mb-8">
        <div className="w-16 h-16 rounded-full bg-blue-600 flex items-center justify-center mb-2 shadow-lg">
          <span className="text-white text-3xl font-bold">JM</span>
        </div>
        <h1 className="text-4xl font-extrabold text-blue-700 mb-2 text-center tracking-tight">JobMate AI</h1>
        <p className="text-lg text-gray-700 mb-2 text-center max-w-lg">
          <span className="font-semibold text-blue-600">Impress recruiters. Land your dream job.</span><br />
          Paste your CV and Job Description below for instant, explainable matching scores and gap analysis.
        </p>
      </div>
      <div className="max-w-2xl w-full bg-white shadow-2xl rounded-2xl p-10 border border-blue-100">
        <div className="mb-4 text-xs text-gray-500 text-right">
          <span className="font-mono bg-blue-50 px-2 py-1 rounded">API: {API}</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">CV (PDF or Text)</label>
            <div className="text-xs text-gray-500 mb-2">PDF upload is for recruiter demo only. Browser cannot extract text—please paste CV text below.</div>
            <div className="flex gap-2 items-center mb-2">
              <input
                type="file"
                accept="application/pdf"
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                onChange={handleCVUpload}
              />
              {cvFileName && <span className="text-xs text-gray-400">{cvFileName}</span>}
            </div>
            <textarea
              className="border border-blue-300 rounded-lg p-3 text-sm resize-none h-32 w-full focus:outline-blue-400 bg-gray-50"
              placeholder="Paste CV text..."
              value={cv}
              onChange={e => setCv(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Job Description</label>
            <textarea
              className="border border-blue-300 rounded-lg p-3 text-sm resize-none h-32 w-full focus:outline-blue-400 bg-gray-50"
              placeholder="Paste Job Description..."
              value={jd}
              onChange={e => setJd(e.target.value)}
            />
          </div>
        </div>
        <button
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg text-lg transition disabled:bg-blue-300 shadow"
          onClick={analyze}
          disabled={loading || !cv || !jd}
        >
          {loading ? "Analyzing..." : "Analyze Match"}
        </button>
        {err && (
          <div className="mt-8 bg-red-100 rounded-xl p-6 border border-red-300">
            <p className="text-red-600 text-center text-lg font-semibold">{err}</p>
          </div>
        )}
        {res && (
          <div className="mt-8 bg-blue-50 rounded-xl p-6 border border-blue-200">
            <h2 className="text-xl font-bold text-blue-700 mb-4 text-center">Match Results</h2>
            <div className="flex flex-col md:flex-row gap-6 justify-center">
              <div className="flex-1">
                <div className="font-semibold mb-1">Score</div>
                <div className="text-2xl text-blue-700 font-bold">{res.score}</div>
              </div>
              <div className="flex-1">
                <div className="font-semibold mb-1">Matches</div>
                <div className="text-green-700">{res.matches?.join(", ") || "None"}</div>
              </div>
              <div className="flex-1">
                <div className="font-semibold mb-1">Gaps</div>
                <div className="text-red-700">{res.gaps?.join(", ") || "None"}</div>
              </div>
            </div>
          </div>
        )}
      </div>
      <footer className="mt-10 text-center text-sm text-muted">
        <p>© {new Date().getFullYear()} JobMateAI. Built by <span className="font-medium text-foreground">Giuseppe</span> for job seekers & recruiters.</p>
        <div className="mt-2 flex justify-center gap-4">
          <a href="https://github.com/Giuseppe552" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600">GitHub</a>
          <a href="https://www.linkedin.com/in/Giuseppe552" target="_blank" rel="noopener noreferrer" className="hover:text-blue-600">LinkedIn</a>
        </div>
      </footer>
    </main>
  );
}
