from typing import Annotated
from fastapi import APIRouter, Body, Path, Query, status
from fastapi.responses import Response, JSONResponse
from sqlalchemy import select

from . import dependencies, schemas, models
from .constants import *

router = APIRouter(
    prefix='/users'
)


@router.get(
    '/',
    response_model=list[schemas.UserRead]
    )
async def get_users(
    manager: dependencies.InjectionUserManager,
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 100,
    role: Annotated[Role, Query()] = None
    ):
    users = await manager.get_all(offset, limit, role)
    return users.scalars()


@router.get(
    '/{username}',
    response_model=schemas.UserRead
    )
async def get_user(
    user: dependencies.InjectionUser
    ):
    return user


@router.post(
    '/',
    response_model=schemas.UserRead
    )
async def create_user(
    manager: dependencies.InjectionUserManager,
    item: schemas.UserCreate
    ):
    user = await manager.create(item)
    return user


@router.post('/{username}/verify')
async def verify(
    username: Annotated[str, Path()],
    manager: dependencies.InjectionUserManager,
    code: Annotated[str, Query()]
    ):
    user = await manager.get_by(models.User.username == username)
    user = user.scalar()
    if not user.verify(code):
        return JSONResponse(
            {"message": "Wrong code or user already verified."},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    manager.session.add(user)
    await manager.session.commit()
    return JSONResponse(
        {"message": "User veirified."},
        status_code=status.HTTP_200_OK
    )


@router.get(
    '/{username}/unverified',
    response_model=list[schemas.UnverifiedUser]
    )
async def get_uverified_users(
    username: Annotated[str, Path()],
    session: dependencies.InjectionSession
    ):
    stmt = select(models.Admin).where(models.Admin.username == username)
    admin = await session.execute(stmt)
    admin = admin.scalar()
    if admin is None:
        return Response(
            {"message": "You are not admin."},
            status_code=status.HTTP_403_FORBIDDEN
        )
    stmt = select(models.User).where(models.User.is_verified == False)
    users = await session.execute(stmt)
    return users.scalars()
        

@router.get(
    '/{admin_username}/unverified/{usrename}',
    response_model=schemas.UnverifiedUser
    )
async def get_uverified_users(
    admin_username: Annotated[str, Path()],
    username: Annotated[str, Path()],
    session: dependencies.InjectionSession
    ):
    stmt = select(models.Admin).where(models.Admin.username == admin_username)
    admin = await session.execute(stmt)
    admin = admin.scalar()
    if admin is None:
        return Response(
            {"message": "You are not admin."},
            status_code=status.HTTP_403_FORBIDDEN
        )
    stmt = select(models.User).where(models.User.is_verified == False, models.User.username == username)
    user = await session.execute(stmt)
    user = user.scalar()
    if user is None:
        return Response(
            {"message": "Unverified user not found."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    return user
