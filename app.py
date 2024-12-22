from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from predict import get_prediction

app = FastAPI()

# Настройка шаблонов
templates = Jinja2Templates(directory="templates")

# Подключение статических файлов
app.mount("/forecasts", StaticFiles(directory="forecasts"), name="forecasts")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, number: int = Form(...)):
    total_population = get_prediction(number)
    formatted_number = "{:,}".format(total_population)
    result = f"Население Беларуси на {number} год составит: {formatted_number}"
    image_url = f"/forecasts/population_forecast_{number}.png"  # Путь к изображению
    return templates.TemplateResponse("main.html", {"request": request, "result": result, "image_url": image_url})