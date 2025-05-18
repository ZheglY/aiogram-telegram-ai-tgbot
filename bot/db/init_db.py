from bot.db.models import Base, engine


async def init_db():
    """
    Initializes the database by creating all tables defined in the metadata.

    This function should be called once during application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)




