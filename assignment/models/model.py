from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from datetime import datetime


# author schema
class CreateAuthor(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    nationality: Annotated[str, Field(max_length=255)]
    DOB: datetime


class AuthorResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    name: str
    nationality: str
    DOB: datetime
    created_at: datetime
    updated_at: datetime


class UpdateAuthor(BaseModel):
    name: Annotated[str | None, Field(max_length=255)] = None
    nationality: Annotated[str | None, Field(default=None, max_length=255)] = None
    DOB: datetime


#  book schema
class CreateBook(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    genre: Annotated[str, Field(max_length=255)]
    author_id: Annotated[str, Field(max_length=255)]
    published_year: datetime


class BookResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    name: str
    genre: str
    author_id: str
    published_year: datetime
    created_at: datetime
    updated_at: datetime


class AuthorListBooks(BaseModel):
    author_id: str
    books: list[BookResponse]
