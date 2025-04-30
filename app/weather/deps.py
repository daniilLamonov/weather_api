from datetime import datetime, time

import httpx
from fastapi import HTTPException, Depends
from fastapi_cache.decorator import cache


base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
api_key = "S8DVYAQSJV5HPK6KZBSWHY2LD"

def from_f_to_c_degrees(farengeit: int) -> int:
    return round((farengeit - 32) / 1.8)

@cache(expire=30)
async def get_weather(location: str):
    url = f"{base_url}{location}?key={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        return HTTPException(status_code=response.status_code)

async def get_weather_today(location: str):
    data = await get_weather(location)
    print(data)
    description = data["description"]
    today = data['days'][0]
    tempmax = from_f_to_c_degrees(today['tempmax'])
    tempmin = from_f_to_c_degrees(today['tempmin'])
    return {"description": description, "tempmin": tempmin, "tempmax": tempmax}

async def get_weather_now(location: str, time_now: datetime):
    data = await get_weather(location)
    time_utc = round(data["tzoffset"] + time_now.hour)
    if time_now.minute > 30:
        time_utc += 1
    now = data['days'][0]["hours"][time_utc]
    temp = from_f_to_c_degrees(now['temp'])
    feelslike = from_f_to_c_degrees(now['feelslike'])
    humidity = now['humidity']
    uvindex = now['uvindex']
    return {"temp": temp, "feelslike": feelslike, "humidity": humidity, "uvindex": uvindex}



