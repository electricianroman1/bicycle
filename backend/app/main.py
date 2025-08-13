from fastapi import FastAPI
from .routes import sheets

app = FastAPI(title="Bicycle LSS API", version="1.0.0")

api = FastAPI()
app.include_router(sheets.router, prefix="/api/v1")
