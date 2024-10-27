from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse
from app.utils.camera_manager import camera_manager
from app.utils.video_streamer import VideoStreamer

import logging

logger = logging.getLogger(__name__)

#Шаблоны страниц html
templates = Jinja2Templates(directory="app/templates")


router = APIRouter(
    prefix="/detect",
    tags=["detection"]
)

@router.get("/stream/{camera_name}")
async def video_feed(camera_name: str):
    logger.info(f"Запрошен видеопоток для камеры: {camera_name}")
    streamer = camera_manager.get_streamer(camera_name)
    if not streamer:
        logger.error(f"Камера с именем {camera_name} не найдена")
        raise HTTPException(status_code=404, detail="Камера не найдена")
    return StreamingResponse(streamer.generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/{camera_name}")
async def video_page(request: Request, camera_name: str):
    """
    Возвращает HTML-страницу с видеопотоком камеры.
    """
    logger.info(f"Запрошена HTML страница для камеры: {camera_name}")
    streamer = camera_manager.get_streamer(camera_name)
    if not streamer:
        logger.error(f"Камера с именем {camera_name} не найдена")
        raise HTTPException(status_code=404, detail="Камера не найдена")
    
    # Возвращаем HTML-страницу с тегом img, где src будет указывать на эндпоинт с видеопотоком
    return templates.TemplateResponse("video_page.html", {"request": request, "camera_name": camera_name})