from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.robot_state import robot_data
from app.task_runner import runner



app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
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
    runner.start_mission()
    return RedirectResponse(url="/", status_code=303)

@app.post("/stop")
def stop_mission():
    runner.stop_mission()
    return RedirectResponse(url="/", status_code=303)

@app.post("/reset")
def reset_robot():
    runner.reset_robot()
    return RedirectResponse(url="/", status_code=303)

@app.post("/obstacle")
def trigger_obstacle():
    runner.trigger_obstacle()
    return RedirectResponse(url="/", status_code=303)

@app.post("/clear_obstacle")
def clear_obstacle():
    runner.clear_obstacle()
    return RedirectResponse(url="/", status_code=303)

@app.post("/set_loop")
def set_loop(loop_count: int = Form(1)):
    robot_data["loop_enabled"] = True
    robot_data["loop_count"] = loop_count
    return RedirectResponse(url="/", status_code=303)
