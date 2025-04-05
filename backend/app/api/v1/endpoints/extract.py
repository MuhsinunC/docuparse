from fastapi import APIRouter

router = APIRouter()

@router.post("") # Route is at /api/v1/extract
async def extract_data(request_body: dict):
    # Placeholder for extract logic (using jobid://)
    return {"message": "Extract placeholder", "input": request_body}

@router.post("/async") # Route is at /api/v1/extract/async
async def extract_data_async(request_body: dict):
    # Placeholder for async extract logic
    return {"message": "Async extract placeholder", "input": request_body} 