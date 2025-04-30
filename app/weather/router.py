from asyncio import sleep

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.weather.deps import get_weather

router = APIRouter()



@router.get("/")
@cache(expire=3600)
async def get_current_weather(location: str):
    data = await get_weather(location)
    return data