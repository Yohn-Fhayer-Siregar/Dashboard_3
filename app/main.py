from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.robot_state import robot_data
from app.task_runner import runner
from app.modbus_client import modbus

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "robot": robot_data,
        },
    )


@app.post("/connect_modbus")
def connect(ip: str = Form(...), port: int = Form(...)):
    ok = modbus.connect(ip, port)
    robot_data["modbus"]["connected"] = ok
    return {"ok": ok}


@app.post("/start")
def start_mission():
    runner.start()
    return RedirectResponse(url="/", status_code=303)


@app.post("/stop")
def stop_mission():
    runner.running = False
    return RedirectResponse(url="/", status_code=303)


@app.post("/reset")
def reset_robot():
    robot_data["status"]["current_point"] = 0
    robot_data["status"]["target_point"] = 0
    return RedirectResponse(url="/", status_code=303)
