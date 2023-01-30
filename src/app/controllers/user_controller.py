from typing import List

from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from starlite import Controller, post, get, HTTPException, Provide
from starlite.status_codes import HTTP_404_NOT_FOUND

from src.app.database.models.user_model import User, UserGetDTO, UserCreateOrLoginDTO


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
