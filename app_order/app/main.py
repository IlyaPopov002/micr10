# uvicorn app.main:app --reload

import asyncio

from app import rabbitmq
from app.endpoints.order_router import order_router, metrics_router
from fastapi import FastAPI
import logging
from logging_loki import LokiHandler

#from app.endpoints.receipt_router import receipt_router
#from app.endpoints.receipt_router import receipt_router

app = FastAPI(title='Service')

#app.include_router(order_router, prefix='/api')
#app.include_router(receipt_router, prefix='/api')

loki_logs_handler = LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"application": "fastapi"},
    version="1",
)
logger = logging.getLogger("uvicorn.access")
logger.addHandler(loki_logs_handler)


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))

app.include_router(order_router, prefix='/api')
app.include_router(metrics_router)
