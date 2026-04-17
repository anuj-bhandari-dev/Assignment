from ariadne import MutationType
from core import LoggerSetup
from db import get_db
from bson import ObjectId
from datetime import datetime

logger = LoggerSetup.setup_logger(__name__)

mutation = MutationType()


@mutation.field("createAuthor")
async def resolve_create_author(_, info, input):
    db = await get_db()
    timestamps = {"created_at": datetime.now(), "updated_at": datetime.now()}
    author_data = {**input, **timestamps}
    result = await db.authors.insert_one(author_data)

    if result.inserted_id:
        created_author = await db.authors.find_one({"_id": result.inserted_id})
        return created_author

    logger.error("Failed to create author")
    return None


@mutation.field("createBook")
async def resolve_create_book(_, info, input):
    db = await get_db()
    timestamps = {"created_at": datetime.now(), "updated_at": datetime.now()}
    book_data = {**input, **timestamps}
    result = await db.books.insert_one(book_data)

    if result.inserted_id:
        created_book = await db.books.find_one({"_id": result.inserted_id})
        return created_book

    logger.error("Failed to create book")
    return None
