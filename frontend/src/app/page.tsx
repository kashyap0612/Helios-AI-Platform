'use client';
import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');

  const run = async () => {
    const res = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query, use_rag: true }) });
    const data = await res.json();
    setAnswer(data.answer ?? JSON.stringify(data));
  };

  return <main className="min-h-screen bg-zinc-950 text-zinc-100 p-8"><h1 className="text-3xl font-bold mb-4">Helios AI Platform</h1><textarea className="w-full h-28 bg-zinc-900 p-3" value={query} onChange={(e)=>setQuery(e.target.value)} /><button className="mt-3 bg-cyan-700 px-4 py-2" onClick={run}>Send</button><pre className="mt-4 bg-zinc-900 p-4 whitespace-pre-wrap">{answer}</pre></main>;
}
