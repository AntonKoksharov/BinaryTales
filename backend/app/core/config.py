import os

class Settings:
    PROJECT_NAME: str = "ФинСмарт API"
    API_V1_PREFIX: str = "/api/v1"
    
    # SQLite для локальной разработки с поддержкой асинхронности (aiosqlite)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./finsmart.db")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "finsmart_super_secret_jwt_key_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    
    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()
