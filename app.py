from fastapi import FastAPI

app = FastAPI(title="Assistant Backend")

@app.get("/")
def root():
 return {"ok": True, "hint": "Use /health"}

@app.get("/health")
def health():
 return {"status": atus": "ok"}
