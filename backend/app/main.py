# backend/app/main.py
from fastapi import FastAPI

app = FastAPI(title="DocuParse Backend")

@app.get("/")
def read_root():
    return {"message": "DocuParse Backend is running"}

# Add other endpoints later, e.g., for parsing
# from .api.v1.endpoints import parse
# app.include_router(parse.router, prefix="/api/v1/parse", tags=["parse"])