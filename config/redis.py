from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"  # Change if Redis is on another server
    REDIS_PORT: int = 6379

 # Load from .env file if available

settings = Settings()
