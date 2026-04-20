from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional
from datetime import datetime


# author schema
class CreateAuthor(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    DOB: datetime
    email: str


class AuthorResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    name: str
    email: str
    DOB: datetime
    created_at: datetime
    updated_at: datetime


class UpdateAuthor(BaseModel):
    name: Optional[Annotated[str, Field(max_length=255)]] = None
    DOB: Optional[datetime] = None
    email: Optional[Annotated[str, Field(max_length=255)]] = None


#  book schema
class CreateBook(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    genre: Annotated[str, Field(max_length=255)]
    author: Annotated[str, Field(max_length=255)]
    published_year: datetime


class BookResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    name: str
    genre: str
    author: str
    published_year: datetime
    created_at: datetime
    updated_at: datetime


class AuthorListBooks(BaseModel):
    author_id: str
    books: list[BookResponse]
