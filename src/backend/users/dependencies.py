from typing import Annotated
from fastapi import Depends, Path, HTTPException

from database import InjectionSession
from . import service, models


async def get_manager(session: InjectionSession):
    yield service.UserManager(session)


async def user_from_path(
    username: Annotated[str, Path()],
    manager: Annotated[service.UserManager, Depends(get_manager)]
    ):
    user = await manager.get_by(
        models.User.username==username
        )
    user = user.scalar()
    if user is None:
        raise HTTPException(
            404
        )
    return user


InjectionUser = Annotated[models.User, Depends(user_from_path)]
InjectionUserManager = Annotated[service.UserManager, Depends(get_manager)]
