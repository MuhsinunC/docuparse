from fastapi import APIRouter

# Import routers from endpoint files
from .endpoints import upload, webhooks, jobs

from .endpoints.parse import sync_router as parse_sync_router
from .endpoints.parse import async_router as parse_async_router

from .endpoints.split import sync_router as split_sync_router
from .endpoints.split import async_router as split_async_router

from .endpoints.extract import sync_router as extract_sync_router
from .endpoints.extract import async_router as extract_async_router

# Create the main v1 router
api_v1_router = APIRouter()

# Include endpoint-specific routers
# The path for each endpoint will be defined here
api_v1_router.include_router(upload.router, prefix="/upload", tags=["Upload"])

api_v1_router.include_router(parse_sync_router, prefix="/parse", tags=["Parse"])
api_v1_router.include_router(parse_async_router, prefix="/parse_async", tags=["Parse"])

api_v1_router.include_router(extract_sync_router, prefix="/extract", tags=["Extract"])
api_v1_router.include_router(extract_async_router, prefix="/extract_async", tags=["Extract"])

api_v1_router.include_router(split_sync_router, prefix="/split", tags=["Split"])
api_v1_router.include_router(split_async_router, prefix="/split_async", tags=["Split"])

api_v1_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

# Add other v1 routes here if needed, or include other sub-routers 