from fastapi import APIRouter
import logging
import sys

print("[BACKEND PRINT - MODULE LEVEL]: Loading NEW parse.py", flush=True, file=sys.stderr)

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("") # Route is at /api/v1/parse
async def parse_document(request_body: dict):
    # Placeholder for synchronous parse logic
    logger.info(f"Received synchronous parse request: {request_body}")
    # Example: Call Reducto /parse endpoint or local parser
    # Need document_url (can be local path, http url, or jobid://)
    document_url = request_body.get("document_url")
    if not document_url:
        # Proper error handling needed here
        return {"error": "document_url is required"}

    # --- Placeholder for actual parsing --- 
    job_id = f"job_{document_url[:10]}" # Dummy job ID
    # --- End Placeholder ---

    return {"message": "Synchronous parse placeholder", "job_id": job_id, "input": request_body}

@router.post("/async") # Route is at /api/v1/parse/async
async def parse_document_async(request_body: dict):
    # Placeholder for asynchronous parse logic
    logger.info(f"Received asynchronous parse request: {request_body}")
    # Example: Call Reducto /parse_async or trigger background task
    document_url = request_body.get("document_url")
    webhook_config = request_body.get("webhook")
    if not document_url:
        # Proper error handling needed here
        return {"error": "document_url is required"}

    # --- Placeholder for async triggering --- 
    job_id = f"async_job_{document_url[:10]}" # Dummy job ID
    # Trigger background processing here...
    # If webhook_config is present, use it.
    # --- End Placeholder ---

    return {"message": "Asynchronous parse placeholder", "job_id": job_id, "input": request_body}

# Remove the old upload logic if it was here
# async def upload_document(...): was moved/deleted 