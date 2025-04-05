from fastapi import APIRouter

# Import routers from endpoint files
from .endpoints import upload, parse, extract, split, webhooks, jobs

# Create the main v1 router
api_v1_router = APIRouter()

# Include endpoint-specific routers
# The path for each endpoint will be defined here
api_v1_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_v1_router.include_router(parse.router, prefix="/parse", tags=["Parse"])
api_v1_router.include_router(extract.router, prefix="/extract", tags=["Extract"])
api_v1_router.include_router(split.router, prefix="/split", tags=["Split"])
api_v1_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# Add other v1 routes here if needed, or include other sub-routers 