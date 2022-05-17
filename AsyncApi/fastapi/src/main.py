import httpx
import logging
import requests as client
import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING
from db import elastic, redis

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['film'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genre'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['person'])


# Проверяет Auth сервис. Обращается по адресу.
# Если в заголовке есть валидный токен, предоставляет доступ к контенту
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    headers = request.headers
    resp = await check_user('http://nginx/auth/v1/usercheck', dict(headers))
    if resp.status_code == 200:
        response = await call_next(request)
        return response
    return Response(status_code=401)


async def check_user(url, headers):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        return resp

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
