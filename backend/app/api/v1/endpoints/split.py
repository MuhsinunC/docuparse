from fastapi import APIRouter

router = APIRouter()

@router.post("") # Route is at /api/v1/split
async def split_document(request_body: dict):
    # Placeholder for split logic
    return {"message": "Split placeholder", "input": request_body} 