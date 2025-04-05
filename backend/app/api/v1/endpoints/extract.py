from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# --- Common Models --- #

# Reusing generic response model for async jobs from parse.py concept
# If structure differs significantly, define a specific one here.
class AsyncJobResponse(BaseModel):
    job_id: str = Field(..., description="The ID assigned to the asynchronous job.")
    message: str = Field(..., description="Confirmation message.")


# --- Synchronous Extract --- #

class ExtractRequest(BaseModel):
    document_url: str = Field(..., description="URL or job ID (e.g., jobid://{parse_job_id}) of the parsed document.")
    schema_: Dict[str, Any] = Field(..., alias="schema", description="The extraction schema definition.")
    options: Optional[Dict[str, Any]] = Field(None, description="Extraction options.")

# Placeholder - actual sync extract returns the extracted data
class ExtractResponse(BaseModel):
    result: Optional[Any] = Field(None, description="Extracted data based on the schema.")
    message: str

@router.post(
    "/", # Route is at /api/v1/extract
    response_model=ExtractResponse, # Placeholder response
    summary="Extract Data (Synchronous)",
    description="(Placeholder) Extracts structured data synchronously based on a schema. Requires `document_url` (often a `jobid://`) and `schema`."
)
async def extract_data(request: ExtractRequest):
    logger.info(f"Received synchronous extract request for: {request.document_url}")
    # --- Placeholder for actual sync extraction --- 
    # TODO: Call sync extractor/Reducto
    # --- End Placeholder ---
    return ExtractResponse(result={"placeholder": "extracted data"}, message="Synchronous extract placeholder response.")

# --- Asynchronous Extract --- #

class AsyncExtractRequest(BaseModel):
    document_url: str = Field(..., description="URL or job ID (e.g., jobid://{parse_job_id}) of the parsed document.")
    schema_: Dict[str, Any] = Field(..., alias="schema", description="The extraction schema definition.")
    options: Optional[Dict[str, Any]] = Field(None, description="Extraction options.")
    webhook: Optional[Dict[str, str]] = Field(None, description="Optional webhook configuration.", example={"mode": "svix"})

@router.post(
    "/async", # Route is at /api/v1/extract/async
    response_model=AsyncJobResponse,
    summary="Extract Data (Asynchronous)",
    description="Initiates an asynchronous job to extract data based on a schema. Returns a job ID.",
    status_code=status.HTTP_202_ACCEPTED
)
async def extract_data_async(request: AsyncExtractRequest):
    logger.info(f"Received asynchronous extract request for: {request.document_url}")
    # --- Placeholder for async triggering --- 
    # TODO: Call async extractor/Reducto
    dummy_job_id = f"async-extract-job-{abs(hash(request.document_url + str(request.schema_)))}"
    # --- End Placeholder ---
    return AsyncJobResponse(job_id=dummy_job_id, message="Asynchronous extract job accepted.") 