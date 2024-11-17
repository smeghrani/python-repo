from fastapi import APIRouter
from starlette import status

router = APIRouter(
    tags=["Health Check"],
    dependencies=[],
    responses={
        200: {"description": "Content generated successfully"},
        400: {"description": "Invalid input"},
        404: {"description": "Not found"},
        500: {"description": "Content generation error"},

    },
)

@router.get("/liveliness", status_code=status.HTTP_200_OK)
async def liveliness():
    return {"status": "alive"}

@router.get("/readiness", status_code=status.HTTP_200_OK)
async def readiness():
    return {"status": "ready"}