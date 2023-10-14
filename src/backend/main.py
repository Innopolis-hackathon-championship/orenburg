import logging

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

import users
import products

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:\t%(name)s %(asctime)s %(message)s'
    )

app = FastAPI()

app.include_router(users.router.router)
app.include_router(products.router.order_router)
app.include_router(products.router.product_router)


@app.route('/')
def index(request: Request) -> HTMLResponse:
    return HTMLResponse('Xd team.')