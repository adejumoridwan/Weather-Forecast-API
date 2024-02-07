from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import convert, predict

app = FastAPI()

# Pydantic Models


class WeatherVariable(BaseModel):
    weather_variable: str


class WeatherValues(WeatherVariable):
    forecast: dict


# Routes


@app.get("/")
async def hello_world():
    return {"Hello": "World!"}


@app.post("/predict", response_model=WeatherValues, status_code=200)
def get_prediction(payload: WeatherVariable):
    weather_variable = payload.weather_variable

    prediction_list = predict(weather_variable)

    if not prediction_list:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {
        "weather_variable": weather_variable,
        "forecast": convert(prediction_list),
    }
    return response_object

"""
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "weather_variable": "meantemp"
}'
"""