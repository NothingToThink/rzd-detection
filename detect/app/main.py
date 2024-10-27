import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routers import detection, camera, ui

app = FastAPI(
    title="Сервис обнаружения дронов",
    description="Веб-сервис для обнаружения дронов с использованием видео",
    version="1.0.0"
)

app.include_router(detection.router)
app.include_router(camera.router)
app.include_router(ui.router)

Instrumentator().instrument(app).expose(app)

logger.info("Приложение FastAPI запущено")
