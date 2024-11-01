from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.routers.health_check_routers import router as health_check_router


app = FastAPI(
    title="Practice Services",
    description="API Endpoints for Practice Services.",
    summary="Practice Services",
    version="1.0.0",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_check_router,
    prefix="/apis/health-check"
)


@app.get("/", include_in_schema=False)
async def main():
    return RedirectResponse('/docs')