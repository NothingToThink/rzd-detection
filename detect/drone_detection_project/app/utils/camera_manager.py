from threading import Thread
from app.utils.video_streamer import VideoStreamer
import logging

logger = logging.getLogger(__name__)

class CameraManager:
    def __init__(self):
        self.cameras = {}

    def add_camera(self, name, source):
        if name in self.cameras:
            raise ValueError(f"Камера с именем '{name}' уже существует.")
        logger.info(f"Добавляем камеру: {name}, источник: {source}")
        streamer = VideoStreamer(source)
        self.cameras[name] = streamer
        logger.info(f"Камера {name} успешно добавлена")

    def get_streamer(self, name):
        logger.info(f"Поиск камеры: {name} в менеджере")
        streamer = self.cameras.get(name)
        if not streamer:
            logger.error(f"Камера {name} не найдена в менеджере")
        return streamer


    def remove_camera(self, name):
        streamer = self.cameras.pop(name, None)
        if streamer:
            streamer.stop()

    def list_cameras(self):
        return list(self.cameras.keys())

camera_manager = CameraManager()
