from typing import List

from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from starlite import Controller, get, HTTPException, delete, Request, put, patch, NotAuthorizedException
from starlite.contrib.jwt import Token
from starlite.status_codes import HTTP_404_NOT_FOUND

from src.app.database.models.user_model import User, UserGetDTO, UserUpdateDTO, UserCreateDTO
from src.app.guards.is_owner_guard import is_owner_guard


class UserController(Controller):
    path = "/users"

    @get(path="{user_id: int}", tags=["User"])
    async def get_user(self, user_id: str, async_session: AsyncSession) -> UserGetDTO:
        """Get a user by its ID and return it.

        If a user with that ID does not exist, return a 404 response
        """
        result = await async_session.scalars(select(User).where(User.id == user_id))
        user: User | None = result.one_or_none()
        if not user:
            raise HTTPException(detail=f"User with ID {user_id} not found", status_code=HTTP_404_NOT_FOUND)
        return user

    @get(tags=["User"])
    async def get_all_users(self, async_session: AsyncSession) -> List[UserGetDTO]:
        """Get all users"""
        res: ScalarResult = await async_session.scalars(select(User))
        return res.fetchmany() if res is not None else HTTPException(status_code=HTTP_404_NOT_FOUND)

    @delete("{user_id: int}", tags=["User"], guards=[is_owner_guard], status_code=200)
    async def delete_user(self, user_id: int, request: Request[User, Token],
                          async_session: AsyncSession) -> NotAuthorizedException | None:
        req_user = request.user

        result = await async_session.scalars(select(User).where(User.id == user_id))
        user: User | None = result.one_or_none()

        if req_user.id != user.id:
            return NotAuthorizedException()

        await async_session.delete(user)
        await async_session.flush()

        return

    @put("/{user_id: int}", tags=["User"], guards=[is_owner_guard])
    async def update_user(self, user_id: int, data: UserUpdateDTO, request: Request[User, Token],
                          async_session: AsyncSession) -> UserGetDTO:
        req_user: User = request.user

        result = await async_session.scalars(select(User).where(User.id == user_id))
        user: User | None = result.one_or_none()

        if req_user.id != user.id:
            return NotAuthorizedException()

        for key, value in data:
            setattr(user, key, value)

        await async_session.commit()
        await async_session.refresh(user)
        return user
