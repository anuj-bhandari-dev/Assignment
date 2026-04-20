from ariadne import MutationType
from assignment.core import LoggerSetup
from assignment.db import get_db
from assignment.models import (
    CreateAuthor,
    UpdateAuthor,
    CreateBook,
    AuthorResponse,
    BookResponse,
)
from datetime import datetime
from bson import ObjectId
from pydantic import ValidationError
from assignment.utils.serialize import serialize_mongo_doc

logger = LoggerSetup.setup_logger(__name__)

mutation = MutationType()


@mutation.field("createAuthor")
async def resolve_create_author(_, info, input):
    try:
        # Validate input using Pydantic model
        validated_input = CreateAuthor(**input)

        db = await get_db()
        timestamps = {"created_at": datetime.now(), "updated_at": datetime.now()}
        author_data = {**validated_input.model_dump(), **timestamps}
        result = await db.authors.insert_one(author_data)

        if not result.inserted_id:
            logger.error("Failed to create author: no inserted_id returned")
            raise Exception("Failed to create author")

        created_author = await db.authors.find_one({"_id": result.inserted_id})
        if not created_author:
            logger.error(
                f"Failed to retrieve author after insert: {result.inserted_id}"
            )
            raise Exception("Failed to retrieve created author")

        # Validate response using Pydantic model
        created_author_response = serialize_mongo_doc(created_author)
        response = AuthorResponse(**created_author_response)
        return response.model_dump(by_alias=True)
    except ValidationError as ve:
        logger.error(f"Validation error creating author: {ve}")
        raise Exception(f"Invalid author data: {ve.errors()}")
    except Exception as e:
        logger.error(f"Error creating author: {str(e)}")
        raise


@mutation.field("createBook")
async def resolve_create_book(_, info, input):
    try:
        # Validate input using Pydantic model
        validated_input = CreateBook(**input)

        db = await get_db()
        timestamps = {"created_at": datetime.now(), "updated_at": datetime.now()}
        book_data = {**validated_input.model_dump(), **timestamps}
        result = await db.books.insert_one(book_data)

        if not result.inserted_id:
            logger.error("Failed to create book: no inserted_id returned")
            raise Exception("Failed to create book")

        created_book = await db.books.find_one({"_id": result.inserted_id})
        if not created_book:
            logger.error(f"Failed to retrieve book after insert: {result.inserted_id}")
            raise Exception("Failed to retrieve created book")

        # Validate response using Pydantic model
        response = BookResponse(**created_book)
        return response.model_dump(by_alias=True)
    except ValidationError as ve:
        logger.error(f"Validation error creating book: {ve}")
        raise Exception(f"Invalid book data: {ve.errors()}")
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}")
        raise


@mutation.field("updateAuthor")
async def resolve_update_author(_, info, input, _id: str):
    try:
        # Validate input using Pydantic model
        validated_input = UpdateAuthor(**input)

        db = await get_db()

        # Convert string ID to ObjectId
        try:
            author_id = ObjectId(_id)
        except Exception as e:
            logger.error(f"Invalid author ID format: {str(e)}")
            raise Exception("Invalid author ID format")

        timestamps = {"updated_at": datetime.now()}
        # Only include non-None fields from validated input
        update_data = {
            k: v for k, v in validated_input.model_dump().items() if v is not None
        }
        update_data.update(timestamps)

        # Use $set operator for proper MongoDB update
        result = await db.authors.find_one_and_update(
            {"_id": author_id}, {"$set": update_data}, return_document=True
        )

        if not result:
            logger.error(f"Author not found: {author_id}")
            raise Exception("Author not found")

        # Validate response using Pydantic model
        response = AuthorResponse(**result)
        return response.model_dump(by_alias=True)

    except ValidationError as ve:
        logger.error(f"Validation error updating author: {ve}")
        raise Exception(f"Invalid author data: {ve.errors()}")
    except Exception as error:
        logger.error(f"Error updating Author: {str(error)}")
        raise


@mutation.field("sendEmail")
async def resolve_send_email(_, info, input):
    redis = info.context["request"].app.state.redis
    job = await redis.enqueue_job("send_email", input["email"])
    return {"success": True, "message": f"Email job queued with ID: {job.job_id}"}
