import os
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

MODEL = os.getenv("MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI(title="Assistant Backend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY manquante")
    msgs = [{"role": "system", "content": "Tu es un assistant concis en français."}]
    if req.history:
        for h in req.history[:10]:
            msgs.append({"role": h.get("role", "user"), "content": h.get("content", "")})
    msgs.append({"role": "user", "content": req.message})
    resp = client.chat.completions.create(model=MODEL, messages=msgs, temperature=0.4)
    return {"answer": resp.choices[0].message.content}

@app.get("/")
def root():
    return {"ok": True, "hint": "Utilisez /health ou POST /chat"}
