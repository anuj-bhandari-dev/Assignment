from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core import DATABASE_URL, LoggerSetup

client: AsyncIOMotorClient = None

logger = LoggerSetup().setup_logger(name="DB connection")


async def init_db():
    global client
    client = AsyncIOMotorClient(DATABASE_URL)
    logger.info("successfull connection")


async def close_db():
    global client
    if client:
        client.close()
        logger.info("DB connection closed.")


async def get_db() -> AsyncIOMotorDatabase:
    return client.MyBooks
