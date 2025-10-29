import os
from fastapi import FastAPI

app = FastAPI(title="Assistant Backend")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/env")
def env():
    return {
        "MODEL": os.getenv("MODEL"),
        "OPENROUTER_API_KEY": bool(os.getenv("OPENROUTER_API_KEY")),
        "OPENROUTER_SITE": os.getenv("OPENROUTER_SITE"),
        "OPENROUTER_TITLE": os.getenv("OPENROUTER_TITLE"),
    }
