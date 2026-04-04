from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.auth import router as auth_router
from .routes.incidents import router as incidents_router
from .routes.tasks import router as tasks_router
from .routes.notifications import router as notifications_router
from ..config import settings

app = FastAPI(title="OpsCenter API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(incidents_router, prefix="/incidents", tags=["incidents"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(notifications_router, prefix="/notifications", tags=["notifications"])


@app.get("/")
def read_root():
    return {"message": "OpsCenter API is running"}
