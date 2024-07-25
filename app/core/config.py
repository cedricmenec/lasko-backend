from pydantic_settings  import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Lasko Backend"
    API_V1_ROOT: str = "/api/v1"
    DEBUG: bool = False

     # Server settings
    PORT: int = 8000

    # WebSocket settings
    WEBSOCKET_HOST: str = "0.0.0.0"
    WEBSOCKET_PORT: int = 8765
    
     # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080", "https://localhost", "https://localhost:8080"]
    
    class Config:
        env_file = ".env"

settings = Settings()