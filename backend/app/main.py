from fastapi import FastAPI
from .config import settings
from .routes import sheets
from .routes import auth

app = FastAPI(title="DnD Character Sheet API", version="1.0")

app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(sheets.router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"message": "DnD Sheets API is running"}
