OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-4o-mini")  # 4o = lettre o, pas 40

# Si la variable n'est pas définie côté Render, on utilise ton URL Render comme valeur par défaut:
OPENROUTER_SITE = os.getenv("OPENROUTER_SITE", "https://assistant-backend-58xa.onrender.com")
OPENROUTER_TITLE = os.getenv("OPENROUTER_TITLE", "Assistant Backend")
