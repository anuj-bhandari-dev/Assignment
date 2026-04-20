from assignment.core import LoggerSetup
from assignment.db import get_db
from datetime import datetime
from assignment.core import LoggerSetup
from assignment.utils.serialize import serialize_mongo_doc

logger = LoggerSetup.setup_logger(__name__)


async def create_user_repo(new_user):
    try:
        # TODO validation
        db = await get_db()
        timestamps = {"created_at": datetime.now(), "updated_at": datetime.now()}
        new_user = {**new_user.model_dump(), **timestamps}
        result = await db.users.insert_one(new_user)

        if not result.inserted_id:
            logger.error("Failed to create user: no inserted_id returned")
            raise Exception("Failed to create user")
        created_user = await db.users.find_one({"_id": result.inserted_id})
        if not created_user:
            logger.error(
                f"Failed to retrieve author after insert: {result.inserted_id}"
            )
            raise Exception("Failed to retrieve created user")

        # Validate response using Pydantic model
        created_user_response = serialize_mongo_doc(created_user)
        # response = AuthorResponse(**created_author_response)
        # return response.model_dump(by_alias=True)
        return created_user_response
    except Exception as e:
        logger.error(f"Error creating author: {str(e)}")
        pass
