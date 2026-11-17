from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import init_db
from app.api.v1.router import api_v1_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Автоматически создаем таблицы в БД при старте приложения
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Бэкенд REST API интеллектуальной платформы личных финансов «ФинСмарт».",
    lifespan=lifespan
)

# Разрешаем CORS, чтобы запросы от фронтенда (HTML/JS) не блокировались браузером
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты версии 1
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["Системные"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "api_v1": settings.API_V1_PREFIX
    }

@app.get("/api/v1/ping", tags=["Системные"])
async def ping():
    return {"status": "ok", "message": "Бэкенд ФинСмарт работает исправно"}
