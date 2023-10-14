from typing import Annotated
from pydantic import BaseModel
from sqlalchemy import Result, select

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends

from config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@' \
    f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=async_engine, 
    expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BaseManager:
    model: Base

    def __init__(self, session: AsyncSession) -> None:
        if not hasattr(self, 'model'):
            raise Exception("Model field is required.")
        self.session: AsyncSession = session
    
    async def get_one(self, pk):
        return await self.session.get(self.model, pk)
    
    async def get_all(self) -> Result:
        return await self.session.execute(select(self.model))
    
    async def get_by(self, criterion) -> Result:
        stmt = select(self.model).where(criterion)
        return await self.session.execute(stmt)
    
    async def create(self, item: BaseModel):
        db_item = self.model(**item.model_dump())
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item
    
    async def delete(self, item):
        await self.session.delete(item)
        await self.session.commit()
    
    async def update(self, item, data: BaseModel):
        for key, value in data.model_dump().items():
            setattr(item, key, value)
        await self.session.commit()
        return item


async def get_session():
    async with SessionLocal() as db:
        yield db


InjectionSession = Annotated[AsyncSession, Depends(get_session)]