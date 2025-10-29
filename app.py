import os
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL", "gemini-1.5-flash-latest")

app = FastAPI(title="Assistant Backend")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] | None = None

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/env")
def env():
    return {"provider":"gemini-rest","has_key":bool(GEMINI_API_KEY),"model":MODEL}

@app.post("/chat")
def chat(req: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY manquante")

    # Construire l'historique pour REST (contenu “parts”)
    contents = []
    if req.history:
        for h in req.history[:10]:
            role = "user" if h.get("role") == "user" else "model"
            contents.append({"role": role, "parts": [{"text": h.get("content","")}]})
    contents.append({"role":"user","parts":[{"text": req.message}]})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": contents, "generationConfig": {"temperature": 0.4}}
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code >= 400:
        # renvoyer l'erreur textuelle pour debug
        raise HTTPException(status_code=r.status_code, detail=r.text)
    data = r.json()
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        text = ""
    return {"answer": text or "Désolé, aucune réponse."}
