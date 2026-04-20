from bson import ObjectId


def serialize_mongo_doc(doc):
    """Convert MongoDB document for Pydantic validation (ObjectId to string)"""
    if not doc:
        return None
    doc_copy = dict(doc)
    if "_id" in doc_copy and isinstance(doc_copy["_id"], ObjectId):
        doc_copy["_id"] = str(doc_copy["_id"])
    return doc_copy
