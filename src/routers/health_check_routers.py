from fastapi import APIRouter
from starlette import status

from src.app_logger import get_logger

logger = get_logger()
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


# Liveliness endpoint
@router.get("/liveliness", status_code=status.HTTP_200_OK)
async def liveliness():
    return {"status": "alive"}


# Readiness endpoint
@router.get("/readiness", status_code=status.HTTP_200_OK)
async def readiness():
    # Perform any internal checks if necessary
    # Since you have no dependencies, just return 200 OK
    return {"status": "ready"}
