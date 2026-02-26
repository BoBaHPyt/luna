FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Делаем скрипт entrypoint исполняемым
RUN chmod +x docker-entrypoint.sh

# Экспортируем порт
EXPOSE 8000

# Запуск через entrypoint скрипт
ENTRYPOINT ["./docker-entrypoint.sh"]
