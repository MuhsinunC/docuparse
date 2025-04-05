from fastapi import APIRouter, HTTPException, status, Body, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging
import sys

print("[BACKEND PRINT - MODULE LEVEL]: Loading parse.py", flush=True, file=sys.stderr)

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Separate routers for sync and async endpoints
sync_router = APIRouter()
async_router = APIRouter()

# --- Common Models (Used by both/or potentially shared) --- #

class Table(BaseModel):
    """Represents a table extracted from a page."""
    bbox: Optional[List[float]] = Field(None, description="Bounding box of the table [x1, y1, x2, y2].")
    data: List[List[Optional[str]]] = Field(..., description="Table data as a list of lists.")
    page_number: int = Field(..., description="Page number where the table was found.")

class Figure(BaseModel):
    """Represents a figure/image extracted from a page."""
    bbox: Optional[List[float]] = Field(None, description="Bounding box of the figure [x1, y1, x2, y2].")
    caption: Optional[str] = Field(None, description="Caption associated with the figure.")
    page_number: int = Field(..., description="Page number where the figure was found.")
    # In a real scenario, might include image data (e.g., base64) or a link

class Page(BaseModel):
    """Represents content extracted from a single page."""
    page_number: int = Field(..., description="The 1-based page number.")
    text: str = Field(..., description="Extracted text content of the page.")
    tables: List[Table] = Field(default_factory=list, description="List of tables extracted from the page.")
    figures: List[Figure] = Field(default_factory=list, description="List of figures/images extracted from the page.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Page-specific metadata.")

class DocumentMetadata(BaseModel):
    """Represents metadata for the entire document."""
    author: Optional[str] = Field(None, description="Document author.")
    creation_date: Optional[str] = Field(None, description="Document creation date.")
    modification_date: Optional[str] = Field(None, description="Document modification date.")
    title: Optional[str] = Field(None, description="Document title.")
    # Add other relevant metadata fields as needed

# --- Synchronous Parse (File Upload Based) --- #

class ParseResponse(BaseModel):
    """Response model for the synchronous /parse endpoint."""
    source_filename: str = Field(..., description="Original filename of the uploaded document.")
    page_count: int = Field(..., description="Total number of pages in the document.")
    pages: List[Page] = Field(..., description="List of pages with their extracted content.")
    metadata: DocumentMetadata = Field(..., description="Extracted document-level metadata.")
    parsing_mode: str = Field(..., description="The mode used for parsing (e.g., 'text_and_tables').")

# Endpoint for synchronous parsing via file upload
@sync_router.post( # Use sync_router
    "/",  # Path relative to the prefix defined in routes.py
    response_model=ParseResponse,
    summary="Parse a document synchronously (Upload)",
    description="Uploads a document (currently PDF) and extracts text, tables, and metadata synchronously. "
                "This endpoint simulates the parsing process and returns structured data.",
    tags=["Parsing"]
)
async def parse_document_upload(
    file: UploadFile = File(..., description="The document file (PDF) to parse."),
    mode: str = Form("text_and_tables", description="Parsing mode (e.g., 'text', 'tables', 'text_and_tables', 'full'). Determines what content is extracted."),
    ocr_enabled: bool = Form(False, description="Whether to force OCR even for text-based PDFs.")
) -> ParseResponse:
    """
    Parses the uploaded document file based on the specified mode.

    - **file**: The document to be processed.
    - **mode**: Specifies the extraction detail ('text', 'tables', 'text_and_tables', 'full').
    - **ocr_enabled**: Flag to enable/disable OCR.

    Returns a detailed JSON structure containing the extracted content and metadata.
    **(Currently returns a dummy response)**
    """
    logger.info(f"Received synchronous parse request for uploaded file: {file.filename}")

    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided.")

    if not file.filename.lower().endswith(".pdf"):
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Only PDF is supported currently.")

    # --- Dummy Response Implementation ---
    dummy_page_1 = Page(
        page_number=1,
        text="This is the simulated extracted text from page 1. It contains various details.",
        tables=[
            Table(
                bbox=[50.0, 100.0, 550.0, 200.0],
                data=[
                    ["Header A", "Header B", "Header C"],
                    ["Row 1, Cell 1", "Row 1, Cell 2", "Row 1, Cell 3"],
                    ["Row 2, Cell 1", "Row 2, Cell 2", "Row 2, Cell 3"],
                ],
                page_number=1
            )
        ],
        figures=[],
        metadata={"rotation": 0}
    )

    dummy_page_2 = Page(
        page_number=2,
        text="Page 2 contains further information but no tables or figures in this example.",
        tables=[],
        figures=[],
        metadata={}
    )

    dummy_metadata = DocumentMetadata(
        author="Simulated Author",
        creation_date="2024-01-01T12:00:00Z",
        modification_date="2024-01-02T15:30:00Z",
        title="Dummy Document Title"
    )

    dummy_response = ParseResponse(
        source_filename=file.filename,
        page_count=2,
        pages=[dummy_page_1, dummy_page_2],
        metadata=dummy_metadata,
        parsing_mode=mode
    )

    return dummy_response


# --- Asynchronous Parse (URL Based) --- #

# Define a generic response model for async jobs
class AsyncJobResponse(BaseModel):
    job_id: str = Field(..., description="The ID assigned to the asynchronous job.")
    message: str = Field(..., description="Confirmation message.")

class AsyncParseRequest(BaseModel):
    document_url: str = Field(..., description="URL or identifier of the document to parse.")
    options: Optional[Dict[str, Any]] = Field(None, description="Parsing options.")
    webhook: Optional[Dict[str, str]] = Field(None, description="Optional webhook configuration.", example={"mode": "svix"})

@async_router.post( # Use async_router
    "/", # Path relative to the prefix defined in routes.py
    response_model=AsyncJobResponse,
    summary="Parse Document Asynchronously (URL)",
    description="Initiates an asynchronous job to parse a document specified by URL. Returns a job ID.",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Parsing"]
)
async def parse_document_async(request: AsyncParseRequest):
    logger.info(f"Received asynchronous parse request for: {request.document_url}")
    # --- Placeholder for async triggering ---
    dummy_job_id = f"async-parse-job-{abs(hash(request.document_url))}"
    # --- End Placeholder ---
    return AsyncJobResponse(job_id=dummy_job_id, message="Asynchronous parse job accepted.")

# Removed old synchronous parse endpoint and its models 