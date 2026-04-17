from ariadne import (
    load_schema_from_path,
    ScalarType,
    make_executable_schema,
    ObjectType,
)
from resolvers import query
from datetime import datetime, date

datetime_scalar = ScalarType("datetime")


@datetime_scalar.serializer
def serialize_datetime(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


author_type = ObjectType("Author")
book_type = ObjectType("Book")

type_defs = load_schema_from_path("./graphql_schema/schema.graphql")

schema = make_executable_schema(
    type_defs, query, author_type, book_type, datetime_scalar
)
