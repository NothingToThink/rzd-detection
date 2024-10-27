import cv2
import logging
from app.utils.predict import process_frame

logger = logging.getLogger(__name__)

class VideoStreamer:
    def __init__(self, source=0):
        """
        Инициализация видеопотока с камеры.
        Параметр `source` — это источник видео: 0 — для веб-камеры ноутбука.
        """
        self.source = int(source)
        self.cap = cv2.VideoCapture(self.source)
        self.running = True

        if not self.cap.isOpened():
            logger.error(f"Не удалось открыть камеру с источником {source}")
            self.running = False
        else:
            logger.info(f"Камера с источником {source} успешно открыта")

    def stop(self):
        """
        Остановка видеопотока и освобождение ресурсов камеры.
        """
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
            logger.info("Камера остановлена")

    def restart_camera(self):
        """
        Перезапуск камеры в случае сбоя.
        """
        logger.warning(f"Перезапуск камеры с источником {self.source}")
        self.stop()
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            logger.error(f"Не удалось перезапустить камеру с источником {self.source}")
            self.running = False
        else:
            self.running = True
            logger.info(f"Камера с источником {self.source} успешно перезапущена")

    def generate_frames(self):
        """
        Генерация кадров с камеры в формате для потоковой передачи.
        Возвращает последовательность кадров в формате JPEG.
        """
        while self.running:
            success, frame = self.cap.read()
            ##logger.info(success)
            if not success:
                logger.error("Ошибка при чтении кадра с камеры")
                self.restart_camera()
                break
            else:
                ##logger.info("Кадр успешно захвачен")
                # отдаем нейронной сети (пока пусто)
                frame = process_frame(frame)
                # Преобразуем кадр в формат JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    logger.error("Ошибка при кодировании кадра в JPEG")
                    continue    

                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        logger.info("Захват кадров завершён")
