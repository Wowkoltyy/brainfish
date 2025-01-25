import os
from main import app
from fastapi.staticfiles import StaticFiles

# Получаем путь к фронтенду из переменной окружения или используем значение по умолчанию
frontend_path = os.getenv('FRONTEND_PATH', '/app/dist')

# Монтируем статические файлы
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("entrypoint:app", host="0.0.0.0", port=8000, reload=True)