from fastapi import FastAPI
from src.routers.health_check_routers import router as health_check_router
from starlette.responses import RedirectResponse
from src.routers.jira_routers import router as jira_router

app = FastAPI(
    title="FastAPI practice",
    description="API Endpoints for FastAPI services.",
    summary="Practice",
    version="1.0.0"
)

app.include_router(
    health_check_router,
    prefix="/api/health-check"
)

app.include_router(
    jira_router,
    prefix="/api/jira"
)

@app.get("/", include_in_schema=False)
async def main():
    return RedirectResponse('/docs')