from ariadne import QueryType
from core import LoggerSetup
from db import get_db
from bson import ObjectId

logger = LoggerSetup.setup_logger(__name__)

query = QueryType()


@query.field("authors")
async def resolve_authors(_, info):
    db = await get_db()
    authors_cursor = db.authors.find()
    logger.info(authors_cursor)
    authors = []
    async for author in authors_cursor:
        author["id"] = str(author["_id"])
        authors.append(author)
    return authors


@query.field("author")
async def resolve_author(_, info, id: str):
    db = await get_db()
    author = await db.authors.find_one({"_id": ObjectId(id)})
    if author:
        author["id"] = str(author["_id"])
    return author


@query.field("books")
async def resolve_books(_, info):
    db = await get_db()
    books_cursor = db.books.find()
    books = []
    async for book in books_cursor:
        book["id"] = str(book["_id"])
        books.append(book)
    return books


@query.field("book")
async def resolve_book(_, info, id: str):
    db = await get_db()
    book = await db.books.find_one()
    if book:
        book["id"] = str(book["_id"])
    return book
