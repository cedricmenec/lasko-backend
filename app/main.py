import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.websockets.server import start_websocket_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_V1_ROOT}/openapi.json",
        version="1.0.0",
    )

    # Set all CORS enabled origins
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    application.include_router(api_router, prefix=settings.API_V1_ROOT)

    return application

app = create_application()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Lasko backend...")
    asyncio.create_task(start_websocket_server(settings.WEBSOCKET_HOST, settings.WEBSOCKET_PORT))

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Lasko backend...")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)