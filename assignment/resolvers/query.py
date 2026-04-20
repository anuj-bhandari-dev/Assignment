from ariadne import QueryType
from assignment.core import LoggerSetup
from assignment.db import get_db
from assignment.models import AuthorResponse, BookResponse
from bson import ObjectId
from pydantic import ValidationError
from assignment.utils.serialize import serialize_mongo_doc

logger = LoggerSetup.setup_logger(__name__)

query = QueryType()


@query.field("authors")
async def resolve_authors(_, info):
    try:
        db = await get_db()
        authors_cursor = db.authors.find()
        authors = []
        async for author in authors_cursor:
            author_data = serialize_mongo_doc(author)
            response = AuthorResponse(**author_data)
            authors.append(response.model_dump(by_alias=True))
        return authors
    except ValidationError as ve:
        logger.error(f"Validation error fetching authors: {ve}")
        raise Exception(f"Invalid author data: {ve.errors()}")
    except Exception as e:
        logger.error(f"Error fetching authors: {str(e)}")
        raise


@query.field("author")
async def resolve_author(_, info, _id: str):
    try:
        db = await get_db()
        try:
            author_id = ObjectId(_id)
        except Exception as e:
            logger.error(f"Invalid author ID format: {str(e)}")
            raise Exception("Invalid author ID format")

        author = await db.authors.find_one({"_id": author_id})
        if not author:
            logger.error(f"Author not found: {author_id}")
            return None
        author_data = serialize_mongo_doc(author)
        response = AuthorResponse(**author_data)
        return response.model_dump(by_alias=True)
    except ValidationError as ve:
        logger.error(f"Validation error fetching author: {ve}")
        raise Exception(f"Invalid author data: {ve.errors()}")
    except Exception as e:
        logger.error(f"Error fetching author: {str(e)}")
        raise


@query.field("books")
async def resolve_books(_, info):
    try:
        db = await get_db()
        books_cursor = db.books.find()
        books = []
        async for book in books_cursor:
            book_data = serialize_mongo_doc(book)
            response = BookResponse(**book_data)
            books.append(response.model_dump(by_alias=True))
        return books
    except ValidationError as ve:
        logger.error(f"Validation error fetching books: {ve}")
        raise Exception(f"Invalid book data: {ve.errors()}")
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}")
        raise


@query.field("book")
async def resolve_book(_, info, _id: str):
    try:
        db = await get_db()
        # Convert string ID to ObjectId
        try:
            book_id = ObjectId(_id)
        except Exception as e:
            logger.error(f"Invalid book ID format: {str(e)}")
            raise Exception("Invalid book ID format")

        book = await db.books.find_one({"_id": book_id})
        if not book:
            logger.error(f"Book not found: {book_id}")
            return None

        book_data = serialize_mongo_doc(book)
        response = BookResponse(**book_data)
        return response.model_dump(by_alias=True)
    except ValidationError as ve:
        logger.error(f"Validation error fetching book: {ve}")
        raise Exception(f"Invalid book data: {ve.errors()}")
    except Exception as e:
        logger.error(f"Error fetching book: {str(e)}")
        raise
