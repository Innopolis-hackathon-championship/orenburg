import random
import string

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .constants import *
from database import BaseManager


class UserManager(BaseManager):
    model = models.User
    
    async def create(self, item: schemas.UserCreate) -> models.User:
        # Выбираем модель соответсвующую роли.
        model = models.role_map[item.role]
        # Генерим аутентификационный код.
        code = random.choices(string.ascii_lowercase, k=5)
        code = ''.join(code)
        db_item = model(**item.model_dump(), code=code)
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item
    
    async def get_all(
        self,
        offset: int,
        limit: int,
        role: Role | None
        ) -> Result:
        stmt = select(models.Customer).offset(offset).limit(limit)
        if role is not None:
            stmt = stmt.filter(models.User.role == role)
        users = await self.session.execute(stmt)
        return users


async def get_courier_queue(
    session: AsyncSession
    ):
    pass