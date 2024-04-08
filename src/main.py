import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from pydantic import BaseModel

from config import REDIS_HOST, REDIS_PORT

app = FastAPI()


class Data(BaseModel):
    phone: str
    address: str


@app.get('/check_data')
async def check_data(phone: str) -> dict:
    if not await redis.exists(phone):
        raise HTTPException(status_code=404, detail='Phone number not found')
    address = await redis.get(phone)
    return {'address': address}


@app.post('/write_data')
async def write_data(data: Data) -> dict:
    await redis.set(data.phone, data.address)
    return {'message': 'successful'}


@app.put('/write_data')
async def write_data(data: Data) -> dict:
    if not await redis.exists(data.phone):
        raise HTTPException(status_code=404, detail='Phone number not found')
    await redis.set(data.phone, data.address)
    return {'message': 'successful'}


@app.on_event("startup")
async def startup():
    global redis
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



