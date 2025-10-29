import os
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

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
    return {"status": "ok"}

@app.get("/env")
def env():
    return {"provider": "gemini", "has_key": bool(GEMINI_API_KEY), "model": MODEL}

@app.post("/chat")
def chat(req: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY manquante")
    genai.configure(api_key=GEMINI_API_KEY)

    # Historique minimal compatible SDK
    history = []
    if req.history:
        for h in req.history[:10]:
            role = "user" if h.get("role") != "assistant" else "model"
            history.append({"role": role, "parts": [h.get("content", "")]})

    try:
        model = genai.GenerativeModel(MODEL)
        chat_session = model.start_chat(history=history)
        resp = chat_session.send_message(req.message)
        text = getattr(resp, "text", None)
        if not text and getattr(resp, "candidates", None):
            parts = resp.candidates[0].content.parts
            text = parts[0].text if parts else ""
        return {"answer": text or "Désolé, aucune réponse."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


