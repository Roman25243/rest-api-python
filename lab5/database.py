import motor.motor_asyncio
from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://mongo_admin:password@mongodb:27017"
)
db = client.book_library
books_collection = db.books


async def init_db():
    count = await books_collection.count_documents({})
    if count == 0:
        await books_collection.insert_many(
            [
                {
                    "title": "Кобзар",
                    "author": "Тарас Шевченко",
                    "year": 1840,
                    "isbn": "978-966-01-0585-5",
                },
                {
                    "title": "Енеїда",
                    "author": "Іван Котляревський",
                    "year": 1798,
                    "isbn": "978-966-10-4104-0",
                },
            ]
        )
