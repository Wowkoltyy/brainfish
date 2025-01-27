from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from database import RedisManager
import os

app = FastAPI()

db = RedisManager(host='localhost', port=6379, db=0)

# Добавляем маршруты из модуля risks

risks = APIRouter(prefix="/risks")

# Указываем путь к статическим файлам (например, к папке src)
app.mount("/static", StaticFiles(directory="src"), name="static")

# Обработка GET-запроса на корень
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Возвращаем HTML-файл (например, popup.html)
    with open(os.path.join("./dist/popup.html")) as f:
        return HTMLResponse(content=f.read())



@risks.get("/blocked-domain.json")
async def get_blocked_domain():
    # Возвращаем JSON-объект с заблокированными доменами
    blocked_domains = db.get_blocked_domains()
    return JSONResponse(content={"blocked_domains": blocked_domains})


# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

