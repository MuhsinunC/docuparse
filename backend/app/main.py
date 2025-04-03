# backend/app/main.py
from fastapi import FastAPI
from .api.v1.endpoints import parse # Import the router

app = FastAPI(title="DocuParse Backend")

@app.get("/")
def read_root():
    return {"message": "DocuParse Backend is running"}

# Include the parsing router
# All routes defined in parse.py will now be under /api/v1/parse
app.include_router(parse.router, prefix="/api/v1/parse", tags=["parse"])