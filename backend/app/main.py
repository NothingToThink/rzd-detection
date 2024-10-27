from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import cv2
import asyncio
import threading
from processor import RailwayTrack
from tracker import EuclideanDistTracker
import time
import logging

from . import models, schemas, database


# Запускаем модель при старте приложения
async def run_video_processing_async():
    await asyncio.to_thread(run_video_processing)

async def lifespan(app: FastAPI):
    print("i am lifespan")
    # Запуск фоновой задачи обработки видео
    video_task = asyncio.create_task(run_video_processing_async())
        
    yield
    
    # Действия при завершении приложения
    print("Приложение завершилось")
    
    # Отмена фоновой задачи при завершении приложения
    video_task.cancel()
    try:
        await video_task
    except asyncio.CancelledError:
        print("Фоновая задача обработки видео была отменена")


app = FastAPI(lifespan=lifespan)

models.Base.metadata.create_all(bind=database.engine)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], #Разрешаем запросы с этого адреса, чтобы  CORS нам не мешал
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Хранение активных соединений
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Обработка входящих сообщений от клиента, пока что ничего
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Dependency для получения сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    print("im hereL init_db")
    db: Session = database.SessionLocal()
    db.query(models.Rail).delete()
    db.commit()

    # Проверяем, есть ли уже данные в таблице
    #rails_count = db.query(models.Rail).count()
    #if rails_count > 0:
    #    db.close()
    #    return  # Данные уже инициализированы
    number = 50

    # Создаём список рельсов
    rails_data = [
        {
            "id": "1",
            "connections": [],
            "status": "inactive",
            "coordinates": {"x1": 100, "y1": 100, "x2": 100, "y2": 400}
        },
        {
            "id": "2",
            "connections": [],
            "status": "inactive",
            "coordinates": {"x1": 100 + number * 1, "y1": 100, "x2": 100 + number * 1, "y2": 400}
        },
        {
            "id": "3",
            "connections": [""],
            "status": "inactive",
            "coordinates": {"x1": 100 + number * 2, "y1": 100, "x2": 100 + number * 2, "y2": 400}
        },
        {
            "id": "4",
            "connections": ["3"],   
            "status": "inactive",    
            "coordinates": {"x1": 100 + number * 2, "y1": 100, "x2": 150 + number * 3, "y2": 400},
            "is_curve": True
        },
        {
            "id": "5",
            "connections": ["3"],   
            "status": "inactive",    
            "coordinates": {"x1": 100 + number * 2, "y1": 200, "x2": 100 + number * 3, "y2": 400},
            "is_curve": True
        },
        {
            "id": "6",
            "connections": [],
            "status": "inactive",
            "coordinates": {"x1": 200 + number * 3, "y1": 100, "x2": 200 + number * 3, "y2": 400}
        },
        {
            "id": "7",
            "connections": [],   
            "status": "inactive",    
            "coordinates": {"x1": 200 + number * 4, "y1": 100, "x2": 200 + number * 4, "y2": 400}
        },
        {
            "id": "8",
            "connections": [],   
            "status": "inactive",
            "coordinates": {"x1": 200 + number * 5, "y1": 100, "x2": 200 + number * 5, "y2": 400}
        }
    ]

    # Добавляем рельсы в базу данных
    for rail_data in rails_data:
        rail = models.Rail(
            id=rail_data["id"],
            connections=rail_data["connections"],
            status=rail_data["status"],
            coordinates=rail_data["coordinates"]
        )
        db.add(rail)
    db.commit()
    db.close()

init_db()

# Функция обратного вызова при изменении статуса пути
def on_status_change(rail_id, status):
    db: Session = database.SessionLocal()
    rail = db.query(models.Rail).filter(models.Rail.id == str(rail_id)).first()
    if rail:
        rail.status = status
        db.commit()
        # Отправляем обновление всем клиентам через WebSocket
        rails = db.query(models.Rail).all()
        rails_data = [schemas.Rail.from_orm(r).dict() for r in rails]
        # Используем asyncio.create_task для запуска корутины из синхронного кода
        asyncio.create_task(manager.broadcast({"type": "update", "rails": rails_data}))
    db.close()

# Функция для запуска обработки видео
def run_video_processing():
    # Создаем объекты RailwayTrack
    track_5 = RailwayTrack(
        5,
        EuclideanDistTracker(),
        EuclideanDistTracker(),
        cv2.createBackgroundSubtractorKNN(history=5000),
        cv2.createBackgroundSubtractorKNN(history=5000),
        230, 320, 860, 960, 130, 200, 450, 550,
        callback=on_status_change  # Передаем функцию обратного вызова
    )

    tracks = {
        'Путь 5': track_5,
    }

    capture = cv2.VideoCapture('data/videos/your_video.mp4')  # Укажите путь к вашему видео

    while True:
        ret, frame = capture.read()
        #time.sleep(5)
        if not ret:
            # Достигнут конец видео, перематываем на начало
            capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        for track in tracks.values():
            track.show_frame(frame)
            print(track.is_free)
            # Статус путей обновляется через callback

        # Опционально: если вы хотите отображать видео
       # cv2.imshow('Frame', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    capture.release()
    #cv2.destroyAllWindows()
# Функция для запуска модели в отдельном потоке
def start_video_processing():
    run_video_processing()

@app.get("/rails", response_model=List[schemas.Rail])
async def get_rails(db: Session = Depends(get_db)):
    rails = db.query(models.Rail).all()
    return rails

@app.put("/rails/{rail_id}/status")
async def update_rail_status(rail_id: str, status: str, db: Session = Depends(get_db)):
    rail = db.query(models.Rail).filter(models.Rail.id == rail_id).first()
    if not rail:
        raise HTTPException(status_code=404, detail="Rail not found")
    rail.status = status
    db.commit()
    # Отправляем обновление всем клиентам
    await manager.broadcast({"type": "update", "rail_id": rail_id, "status": status})
    return {"message": "Status updated"}
