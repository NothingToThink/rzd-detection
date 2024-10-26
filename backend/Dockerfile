# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем директорию app в контейнер
COPY ./app /app/app

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH=/

# Открываем порт 8000
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
