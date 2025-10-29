import os
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# Clé et modèle (OpenRouter)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-4o-mini") # attention: c'est 4o (lettre o), pas 40

app = FastAPI(title="Assistant Backend")
app.add_middleware(
 CORSMiddleware,
 allow_origins=["*"],
 allow_methods=["*"],
 allow_headers=["*"],
)

class ChatRequest(BaseModel):
 message: str
 history: List[Dict[str, str]] | None = None

@app.get("/")
def root():
 return {"ok": True, "hint": "Use /health, /env, or POST /chat"}

@app.get("/health")
def health():
 return {"status": "ok"}

@app.get("/env")
def env():
 return /env")
def env():
 return rn {"provider": "openrouter", "has_key": bool(OPENROUTER_API_KEY), "model": MODEL}

@app.post("/chat")
def chat(req: ChatRequest):
 if not OPENROUTER_API_KEY:
 raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY manquante (Render > Settings > Environment).")

 msgs = [{"role": "system", "content": "Tu es un assistant concis en français."}]
 if req.history:
 for h in req.history[:10]:
 msgs.append({"role": h.get("role", "user"), "content": h.get("content", "")})
 msgs.append({"role": "user", "content": req.message})

 r = requests.post(
 req.message})

 r = requests.post(
 t(
 "https://openrouter.ai/api/v1/chat/completions",
 headers={
 "Authorization": f"Bearer {OPENROUTER_API_KEY}",
 "Content-Type": "application/json",
 },
 json={"model": MODEL, "messages": msgs, "temperature": 0.4},
 timeout=30
 )
 if r.status_code >= 400:
 raise HTTPException(status_code=r.status_code, detail=r.text)
 data = r.json()
 ans = data["choices"][0]["message"]["content"]
 return {"answer": ans}
