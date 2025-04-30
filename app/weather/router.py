from datetime import datetime, timezone

from fastapi import APIRouter
from starlette.requests import Request

from app.weather.deps import get_weather_today, get_weather_now

router = APIRouter(prefix="/weather", tags=["weather"])



@router.get("/{location}/today")
async def get_current_weather(location: str):
    return await get_weather_today(location)

@router.get("/{location}/now")
async def get_current_weather_now(request: Request, location: str):
    now = datetime.now(timezone.utc)
    return await get_weather_now(location, now)
