import logging

from fastapi import FastAPI, APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

import users
import products

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:\t%(name)s %(asctime)s %(message)s'
    )

app = FastAPI()
# app.add_middleware(HTTPSRedirectMiddleware)
api_router = APIRouter(
    prefix='/api'
)

api_router.include_router(users.router.router)
api_router.include_router(users.router.courier_router)
api_router.include_router(products.router.order_router)
api_router.include_router(products.router.product_router)

app.include_router(api_router)

@app.route('/')
def index(request: Request) -> HTMLResponse:
    return HTMLResponse('Xd team.')