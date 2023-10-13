from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends

from config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@' \
    f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

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
    

async def get_session():
    async with SessionLocal() as db:
        yield db


InjectionSession = Annotated[AsyncSession, Depends(get_session)]