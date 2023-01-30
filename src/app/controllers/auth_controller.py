from datetime import timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlite import ASGIConnection, post, NotAuthorizedException, Request, Response
from starlite.contrib.jwt import Token, JWTAuth, JWTCookieAuth
from starlite.status_codes import HTTP_401_UNAUTHORIZED

from src.app.database.models.user_model import User, UserCreateOrLoginDTO, UserGetDTO
from src.app.database.setup_db import sqlalchemy_plugin, sqlalchemy_config


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User | None:
    user_sub = token.sub
    if user_sub:
        async with sqlalchemy_config.session_maker() as sess:
            res = await sess.scalars(select(User).where(User.name == user_sub))
            req_user: User | None = res.one_or_none()
            return req_user
    return None


jwt_cookie_auth = JWTCookieAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret="123455",
    exclude=["/schema", "/login", "/register"],
    secure=True
)


@post("/login", tags=["Auth"])
async def login_handler(request: Request, data: UserCreateOrLoginDTO, async_session: AsyncSession) -> Response[Any]:
    res = await async_session.scalars(select(User).where(User.name == data.name))
    req_user: User | None = res.one_or_none()

    if not req_user:
        raise NotAuthorizedException(detail=f"User with ID {data.name} not found", status_code=HTTP_401_UNAUTHORIZED)
    elif req_user.password != data.password:
        raise NotAuthorizedException(detail=f"Invalid password for user {data.name}", status_code=HTTP_401_UNAUTHORIZED)

    response = jwt_cookie_auth.login(identifier=data.name, token_expiration=timedelta(days=1))
    return response


@post("/register", tags=["Auth"])
async def register_user(data: UserCreateOrLoginDTO, async_session: AsyncSession) -> UserGetDTO:
    user: User = data.to_model_instance()  # type: ignore[attr-defined]
    async_session.add(user)
    await async_session.commit()
    return user
