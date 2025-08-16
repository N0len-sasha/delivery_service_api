FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-root

COPY . .

# Если есть скрипт запуска, можешь оставить его
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# В качестве CMD пусть запускается uvicorn (или любой основной процесс)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
