from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Define TWO separate routers
sync_router = APIRouter()
async_router = APIRouter()

# --- Common Models --- #

class SplitDescriptionItem(BaseModel):
    name: str
    description: str
    partition_key: Optional[str] = None

# Reusing generic response model for async jobs from parse.py concept
class AsyncJobResponse(BaseModel):
    job_id: str = Field(..., description="The ID assigned to the asynchronous job.")
    message: str = Field(..., description="Confirmation message.")

# --- Synchronous Split --- #

# Based on Reducto Split examples, sync might return results directly.
# Defining placeholder models for now.
class SyncSplitRequest(BaseModel):
    # Sync split might also need descriptions, similar to async?
    # For now, using document_url as per other sync endpoints.
    document_url: str = Field(..., description="URL or job ID (e.g., jobid://{parse_job_id}) of the document to split.")
    split_description: List[SplitDescriptionItem] = Field(..., description="Descriptions of how to categorize pages.")
    split_rules: Optional[Dict[str, Any]] = Field(None, description="Optional rules to modify splitting behavior.")

class SyncSplitResponse(BaseModel):
    # Reducto examples show a 'result' field with 'section_mapping'
    result: Optional[Dict[str, Any]] = Field(None, description="Result of the split operation, e.g., section mapping.")
    usage: Optional[Dict[str, Any]] = Field(None, description="Usage statistics, e.g., page count.")
    message: str

# Use the sync_router
@sync_router.post(
    "/", # Will be mounted at /api/v1/split
    response_model=SyncSplitResponse,
    summary="Split Document (Synchronous)",
    description="(Placeholder) Splits a document synchronously based on descriptions and rules. Requires prior parsing. Returns results directly."
)
async def split_document(request: SyncSplitRequest):
    logger.info(f"Received synchronous split request for: {request.document_url}")
    # --- Placeholder for actual sync split --- 
    # TODO: Call sync splitter/Reducto equivalent
    dummy_result = {
        "section_mapping": {
            f"{desc.name} {desc.partition_key or ''}".strip(): [1, 2]
            for desc in request.split_description
        }
    }
    dummy_usage = {"num_pages": 10} # Example usage
    # --- End Placeholder ---
    return SyncSplitResponse(
        result=dummy_result,
        usage=dummy_usage,
        message="Synchronous split placeholder response."
    )

# --- Asynchronous Split --- #

class AsyncSplitRequest(BaseModel):
    document_url: str = Field(..., description="The URL or job ID (e.g., jobid://{parse_job_id}) of the document to split.")
    split_description: List[SplitDescriptionItem] = Field(..., description="Descriptions of how to categorize pages.")
    split_rules: Optional[Dict[str, Any]] = Field(None, description="Optional rules to modify splitting behavior.")
    webhook: Optional[Dict[str, str]] = Field(None, description="Optional webhook configuration (e.g., {'mode': 'svix'}).", example={"mode": "svix"})

# Use the async_router
@async_router.post(
    "/", # Will be mounted at /api/v1/split_async
    response_model=AsyncJobResponse,
    summary="Split Document (Asynchronous)",
    description="Initiates an asynchronous job to split a document based on provided descriptions and rules. Requires prior parsing. Returns a job ID for status polling.",
    status_code=status.HTTP_202_ACCEPTED # Indicate the request is accepted for processing
)
async def split_document_async(request: AsyncSplitRequest):
    logger.info(f"Received asynchronous split request for: {request.document_url}")

    # --- Placeholder for async triggering --- 
    # TODO: Call the actual async splitting service (e.g., Reducto's /split or equivalent)
    #       using request.document_url, request.split_description, etc.
    # TODO: Store the job ID and its status (e.g., in a database or cache)

    # Generate a dummy job ID (consider a more robust method later)
    dummy_job_id = f"async-split-job-{abs(hash(request.document_url + str(request.split_description)))}"

    # Log received data (for debugging during development)
    if request.split_rules:
        logger.info(f"Split rules: {request.split_rules}")
    if request.webhook:
        logger.info(f"Webhook config: {request.webhook}")

    return AsyncJobResponse(
        job_id=dummy_job_id,
        message="Asynchronous document splitting job accepted."
    ) 