from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.core.config import settings
from app.weather.router import router as weather_router

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0")
    FastAPICache.init(RedisBackend(redis), prefix='cache')
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(weather_router)