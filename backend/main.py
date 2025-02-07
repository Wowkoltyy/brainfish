from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import os

from database import RedisManager


app = FastAPI()

db = RedisManager(host='localhost', port=6379, db=0)

reports = RedisManager(host='localhost', port=6380, db=1)

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

@risks.get("/current-revision")
async def get_current_revision():
    # Возвращаем текущую ревизию приложения
    current_revision = db.get_value("current_revision")
    return JSONResponse(content={"current_revision": current_revision})

@risks.get("/whitelisted-domain.json")
async def get_whitelisted_domain():
    # Возвращаем JSON-объект с разрешёнными доменами
    whitelisted_domains = db.get_whitelisted_domains()
    return JSONResponse(content={"whitelisted_domains": whitelisted_domains})

@risks.get("/blocked-assets.json")
async def get_blocked_assets():
    # Возвращаем JSON-объект с заблокированными ресурсами
    blocked_assets = db.get_blocked_assets()
    return JSONResponse(content={"blocked_asstets": blocked_assets})

@risks.get("/fishing-signs.json")
async def get_fishing_signs():
    # Возвращаем JSON-объект с предупреждениями о знаках о том, что сайт может быть фишинговым
    fishing_signs = db.get_value("fishing_signs")
    return JSONResponse(content={"fishing_signs": fishing_signs})

api = APIRouter(prefix="/api")


@api.post("/report", status_code=204)
async def report_risk(report: dict):
    reports.add_to_set(JSONResponse(dict))

@api.post("/allow", status_code=204)
async def allow(data: dict):
    if data['url'] in db.get_whitelisted_domains(): return
    if data['url'] in db.get_blocked_domains(): return JSONResponse(content = {"message": "Domain is blocked"})

    blocked_asstes = await get_blocked_assets()
    if blocked_asstes in data["hash"]: return JSONResponse(content = {"message": "Domain contains blocked asset"})

    fishing_signs = await get_fishing_signs()

    for fishing_sign in fishing_signs:
        for script in data['contents']:
            if fishing_sign in data['contents'][script]:
                return JSONResponse(content = {"message": "Domain contains fishing sign"})
            
    return
        
    



# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

