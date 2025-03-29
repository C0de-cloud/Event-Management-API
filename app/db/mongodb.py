from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()

client = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    
    await db.events.create_index("title")
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    await db.categories.create_index("name", unique=True)
    await db.venues.create_index("name")
    await db.venues.create_index([("location.coordinates", "2dsphere")])


async def close_mongo_connection():
    global client
    if client:
        client.close()


def get_database():
    return db 