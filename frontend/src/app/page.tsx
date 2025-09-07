"use client";
import { useState } from "react";
import axios from "axios";

const API = process.env.NEXT_PUBLIC_API_URL!; // set on Vercel

export default function Home() {
  const [cv, setCv] = useState("");
  const [jd, setJd] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function analyze() {
    setLoading(true);
    const r = await axios.post(`${API}/score`, { cv_text: cv, jd_text: jd });
    setResult(r.data);
    setLoading(false);
  }

  return (
    <main className="min-h-screen p-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold">JobMate AI</h1>
      <p className="text-sm text-gray-500">Paste CV and Job Description. Get a score with matches & gaps.</p>
      <div className="grid md:grid-cols-2 gap-4 mt-6">
        <textarea className="border p-3 h-64" placeholder="Paste CV text..." value={cv} onChange={e=>setCv(e.target.value)} />
        <textarea className="border p-3 h-64" placeholder="Paste Job Description..." value={jd} onChange={e=>setJd(e.target.value)} />
      </div>
      <button onClick={analyze} disabled={loading} className="mt-4 px-4 py-2 rounded bg-black text-white">
        {loading ? "Analyzing..." : "Analyze Match"}
      </button>
      {result && (
        <div className="mt-6 border p-4 rounded">
          <div className="text-xl font-semibold">Score: {result.score}</div>
          <div className="mt-2">
            <h3 className="font-medium">Top Matches</h3>
            <ul className="list-disc ml-6">{result.matches.map((m:string)=> <li key={m}>{m}</li>)}</ul>
          </div>
          <div className="mt-2">
            <h3 className="font-medium">Top Gaps</h3>
            <ul className="list-disc ml-6">{result.gaps.map((g:string)=> <li key={g}>{g}</li>)}</ul>
          </div>
        </div>
      )}
    </main>
  );
}
