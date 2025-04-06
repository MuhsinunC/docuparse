from fastapi import APIRouter, File, UploadFile, HTTPException
import logging
import sys
import uuid
import os
import shutil
from pathlib import Path

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define upload directory relative to the app's location (assuming app runs from /app)
# Use environment variable if set, otherwise default to /app/uploads
UPLOAD_DIR_STR = os.getenv("UPLOAD_DIR", "/app/uploads")
UPLOAD_DIR = Path(UPLOAD_DIR_STR)

router = APIRouter()

@router.post("") # Actual route is /api/v1/upload
async def upload_document(file: UploadFile = File(...)):
    """
    Receives a document upload, saves it with a unique ID,
    and returns the generated file ID.
    """
    if not file.filename:
        logger.error("Received upload request with no filename.")
        raise HTTPException(status_code=400, detail="No filename provided in upload.")

    print(f"Received file upload: {file.filename}, Content-Type: {file.content_type}")
    logger.info(f"Received file upload request for {file.filename}")

    # Ensure upload directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Generate a unique file ID and construct the path
    file_id = f"file_{uuid.uuid4()}"
    # Preserve the original extension if available
    file_extension = Path(file.filename).suffix
    save_path = UPLOAD_DIR / f"{file_id}{file_extension}"

    try:
        # Save the uploaded file
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Successfully saved file {file.filename} to {save_path} with ID {file_id}")

    except Exception as e:
        logger.error(f"Error saving file {file.filename} (ID: {file_id}): {e}")
        # Attempt to remove partially saved file if error occurs
        if save_path.exists():
            try:
                os.remove(save_path)
            except OSError as rm_err:
                logger.error(f"Failed to remove partially saved file {save_path}: {rm_err}")
        raise HTTPException(status_code=500, detail=f"Could not save uploaded file: {e}")
    finally:
        # file.file is the actual file-like object managed by UploadFile
        # UploadFile's context manager handles closing, no need for await file.close() here
        pass


    # Return the unique file ID
    return {
        "file_id": file_id,
        "original_filename": file.filename,
        "content_type": file.content_type
    } 