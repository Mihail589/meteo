FROM python:3.12-slim

# Устанавливаем рабочую директорию (лучше не в корень)
WORKDIR /
# Устанавливаем компилятор и заголовки PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY server.py .
COPY utilitis /utilitis
COPY templates /templates
COPY static /static

# Команда запуска (замените на ваш основной файл, если не server.py)
CMD ["python", "server.py"]