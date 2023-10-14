import random
import string
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, dependencies, models


async def add_products_to_order(
    session: AsyncSession,
    order: models.Order,
    products_in_cart: list[schemas.ProductInCart]
    ):
    products_in_order = []
    for item in products_in_cart:
        pr_to_ord = models.ProductToOrder(
            order_id = order.id,
            product_id=item.id,
            amount=item.amount,
        )
        products_in_order.append(pr_to_ord)
        session.add(pr_to_ord)
    await session.commit()


def generate_code():
    code = random.choices(string.digits, k=5)
    code = ''.join(code)
    return code