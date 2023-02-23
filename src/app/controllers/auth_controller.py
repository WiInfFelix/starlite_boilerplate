from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlite import ASGIConnection, post, NotAuthorizedException, Request, Response
from starlite.contrib.jwt import Token, JWTCookieAuth
from starlite.status_codes import HTTP_401_UNAUTHORIZED

from src.app.database.models.user_model import User, UserCreateDTO, UserGetDTO, UserLoginDTO
from src.app.database.setup_db import sqlalchemy_config
from src.app.util.crypt import encrypt_password, verify_password


async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> User | None:
    user_sub = token.sub
    if user_sub:
        async with sqlalchemy_config.session_maker() as sess:
            res = await sess.scalars(select(User).where(User.name == user_sub))
            req_user: User | None = res.one_or_none()
            return req_user
    return None


jwt_cookie_config = JWTCookieAuth[User](
    retrieve_user_handler=retrieve_user_handler,
    token_secret="this_should_be_env_imported_and_safe",
    exclude=["/schema", "/login", "/register"],
    secure=True
)


@post("/login", tags=["Auth"])
async def login_handler(request: Request, data: UserLoginDTO, async_session: AsyncSession) -> Response[Token]:
    res = await async_session.scalars(select(User).where(User.email == data.email))
    req_user: User | None = res.one_or_none()

    if not req_user:
        raise NotAuthorizedException(detail=f"User with ID {data.email} not found", status_code=HTTP_401_UNAUTHORIZED)
    elif not verify_password(data.password, req_user.password):  # type: ignore
        raise NotAuthorizedException(detail=f"Invalid password for user {data.email}",
                                     status_code=HTTP_401_UNAUTHORIZED)

    response = jwt_cookie_config.login(identifier=data.email, token_expiration=timedelta(days=1))
    return response


@post("/register", tags=["User"])
async def register_user(data: UserCreateDTO, async_session: AsyncSession) -> UserGetDTO:
    user: User = data.to_model_instance()
    user.password = encrypt_password(user.password)  # type: ignore
    async_session.add(user)
    await async_session.commit()
    return user
