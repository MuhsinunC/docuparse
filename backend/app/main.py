# backend/app/main.py
from fastapi import FastAPI
# Import the central v1 router
from .api.v1.routes import api_v1_router

app = FastAPI(title="DocuParse Backend - Reducto API Mirror")

@app.get("/")
def read_root():
    return {"message": "DocuParse Backend (Reducto Mirror) is running"}

# Include the main v1 router
# All routes defined in routes.py (which includes routes from endpoint files)
# will be available under the /api/v1 prefix
app.include_router(api_v1_router, prefix="/api/v1")