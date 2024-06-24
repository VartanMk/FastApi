# Dockerfile
FROM python:3.9

WORKDIR /app

# Копируем зависимости проекта (requirements.txt, setup.py)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем все остальные файлы проекта
COPY . .

# Запускаем приложение
CMD ["python", "app.py"]
