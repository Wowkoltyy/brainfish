# Stage 1: Build frontend
FROM node:22 as frontend-builder

WORKDIR /app

# Копируем все файлы проекта
COPY . .
COPY backend/database .
RUN npm install
RUN npm run build

# Stage 2: Python runtime
FROM python:3.12-slim


WORKDIR /app
COPY /backend/database.py . 
# Копируем все файлы проекта
COPY . .

# Копируем собранные файлы фронтенда из стадии сборки

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "fastapi[standard]"
# Открываем порт, на котором работает приложение
EXPOSE 8080


# Команда для запуска приложения
#RUN cd  /app/backend
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
#CMD ["fastapi", "dev" , "main.py"]