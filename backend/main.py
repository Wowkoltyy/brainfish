from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Указываем путь к статическим файлам (например, к папке src)
app.mount("/static", StaticFiles(directory="src"), name="static")

# Обработка GET-запроса на корень
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Возвращаем HTML-файл (например, popup.html)
    with open(os.path.join("popup.html")) as f:
        return HTMLResponse(content=f.read())

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
