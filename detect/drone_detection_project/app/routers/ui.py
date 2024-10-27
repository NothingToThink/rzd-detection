from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    tags=["UI"]
)

@router.get("/add-camera", response_class=HTMLResponse)
async def add_camera_form():
    return templates.TemplateResponse("add_camera.html", {"request": {}})
