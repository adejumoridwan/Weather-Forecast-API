from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import uvicorn

from model import convert, predict

templates = Jinja2Templates(directory="templates")

app = FastAPI()


# Pydantic Models
class WeatherVariable(BaseModel):
    weather_variable: str
    days: int


# Routes
@app.get("/", response_class=HTMLResponse)
def go_to_page(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post(
    "/predict",
    response_class=HTMLResponse,
    status_code=200,
)
async def get_prediction(
    request: Request, weather_variable: str = Form(...), days: int = Form(...)
):
    prediction_list = predict(weather_variable, days)

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {
        "weather_variable": weather_variable,
        "forecast": convert(prediction_list),
    }
    return templates.TemplateResponse(
        request, "index.html", {"response": response_object}, status_code=200
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
