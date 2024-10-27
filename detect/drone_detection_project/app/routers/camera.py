from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal, Camera
from app.utils.camera_manager import camera_manager
import logging

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/camera",
    tags=["camera"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add")
def add_camera(name: str, source: str, db: Session = Depends(get_db)):
    logger.info(f"Добавление камеры: {name} с источником: {source}")
    db_camera = db.query(Camera).filter(Camera.name == name).first()
    if db_camera:
        logger.error(f"Камера с именем {name} уже существует")
        raise HTTPException(status_code=400, detail="Камера с таким именем уже существует")

    new_camera = Camera(name=name, source=source)
    db.add(new_camera)
    db.commit()
    db.refresh(new_camera)
    camera_manager.add_camera(name, source)
    logger.info(f"Камера {name} успешно добавлена")
    return {"message": f"Камера '{name}' успешно добавлена."}


@router.get("/list")
def list_cameras(request: Request, db: Session = Depends(get_db)):
    cameras = db.query(Camera).all()
    return templates.TemplateResponse("camera_list.html", {"request": request, "cameras": cameras})