# Стадия 1: Сборка зависимостей
FROM python:3.10.14-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /install

# Устанавливаем системные зависимости и pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmariadb-dev \
        gcc \
        libc-dev \
        g++ \
        libffi-dev \
        libxml2 \
        unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Стадия 2: Финальный образ
FROM python:3.10.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Копируем только runtime зависимости из builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Устанавливаем только runtime системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmariadb3 \
        libxml2 \
        unixodbc \
    && rm -rf /var/lib/apt/lists/*

# Копируем код приложения
COPY . .

CMD ["python", "-u", "main.py"]