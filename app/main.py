import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import websockets

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.websockets.server import websocket_server

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

async def start_websocket_server():
    await websockets.serve(
        websocket_server.handle_connection,
        settings.WEBSOCKET_HOST,
        settings.WEBSOCKET_PORT
    )

@app.on_event("startup")
async def startup_event():
    # You can add any startup logic here
    print("Starting up Lasko backend...")
    asyncio.create_task(start_websocket_server())

@app.on_event("shutdown")
async def shutdown_event():
    # You can add any shutdown logic here
    print("Shutting down Lasko backend...")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)