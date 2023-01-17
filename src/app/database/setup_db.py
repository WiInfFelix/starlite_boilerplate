from sqlalchemy.orm import declarative_base
from starlite import DTOFactory
from starlite.plugins.sql_alchemy import SQLAlchemyConfig, SQLAlchemyPlugin

Base = declarative_base()

sqlalchemy_config = SQLAlchemyConfig(
    connection_string="sqlite+aiosqlite:///test.sqlite", dependency_key="async_session"
)
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
dto_factory = DTOFactory(plugins=[sqlalchemy_plugin])


async def on_startup() -> None:
    async with sqlalchemy_config.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
