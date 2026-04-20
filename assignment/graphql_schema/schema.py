from ariadne import (
    load_schema_from_path,
    ScalarType,
    make_executable_schema,
    ObjectType,
)
from pathlib import Path
from assignment.resolvers import query, mutation
from datetime import datetime, date
from assignment.db import get_db
from bson import ObjectId

datetime_scalar = ScalarType("datetime")


@datetime_scalar.serializer
def serialize_datetime(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


author_type = ObjectType("Author")
book_type = ObjectType("Book")


@book_type.field("author")
async def resolve_book_author(book, info):
    # Resolve the author field on a Book by fetching the author from the database
    if not book.get("author"):
        return None

    db = await get_db()
    author_id = book.get("author")

    if isinstance(author_id, str):
        try:
            author_id = ObjectId(author_id)
        except Exception:
            return None

    author = await db.authors.find_one({"_id": author_id})
    if author:
        return {
            "_id": str(author["_id"]),
            "name": author.get("name"),
            "DOB": author.get("DOB"),
        }
    return None


schema_path = Path(__file__).resolve().parent / "schema.graphql"
type_defs = load_schema_from_path(schema_path)

schema = make_executable_schema(
    type_defs, query, mutation, author_type, book_type, datetime_scalar
)
