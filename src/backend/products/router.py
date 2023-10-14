from typing import Annotated
from fastapi import APIRouter, Path, Query
from sqlalchemy import select

from . import schemas, dependencies, models, constants, service
import users

order_router = APIRouter(
    prefix='/order'
)

product_router = APIRouter(
    prefix='/products'
)


@product_router.get(
    '/',
    response_model=list[schemas.Product]
    )
async def get_all_products(session: dependencies.InjectionSession):
    stmt = select(models.Product)
    products = await session.execute(stmt)
    products = products.scalars()
    return products


@product_router.get(
    '/{id}',
    response_model=schemas.Product
    )
async def get_product(
    id: Annotated[int, Path()],
    session: dependencies.InjectionSession):
    stmt = select(models.Product).where(models.Product.id == id)
    product = await session.execute(stmt)
    product = product.scalar()
    return product


@product_router.post(
    '/',
    response_model=schemas.Product
    )
async def create_product(
    session: dependencies.InjectionSession,
    product_item: schemas.CreateProduct
    ):
    product = models.Product(**product_item.model_dump())
    session.add(product)
    await session.commit()
    return product


@product_router.delete('/{id}')
async def delete_product(
    id: Annotated[int, Path()],
    session: dependencies.InjectionSession
    ):
    stmt = select(models.Product).where(models.Product.id == id)
    product = await session.execute(stmt)
    product = product.scalar()
    await session.delete(product)
    await session.commit()
    return


@order_router.post(
    '/',
    response_model=schemas.Order
    )
async def create_order(
    session: dependencies.InjectionSession,
    order_item: schemas.CreateOrder
    ):
    user = await users.service.UserManager(session).get_by(users.models.User.username == order_item.customer_username)
    user = user.scalar()
    order = models.Order(
        customer_id = user.id,
        status = constants.OrderStatus.prepare,
        delivery_address = order_item.delivery_address,
        code=service.generate_code()
    )
    await service.add_products_to_order(
        session, 
        order,
        order_item.products
        )
    session.add(order)
    await session.commit()
    return order


@order_router.post(
    '/{id}/status'
    )
async def set_status(
    session: dependencies.InjectionSession,
    id: Annotated[int, Path()],
    status: Annotated[constants.OrderStatus, Query()]
    ):
    order: models.Order = service.get_order(session, id)
    order.status = status
    await session.commit()
    