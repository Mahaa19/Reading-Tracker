import datetime

from pydantic import BaseModel, ConfigDict

from app.models import BookStatus


class BookCreate(BaseModel):
	title: str
	author: str
	total_pages: int | None = None
	status: BookStatus = BookStatus.to_read

class BookUpdate(BaseModel):
	title: str | None = None
	author: str | None = None
	total_pages: int | None = None
	status: BookStatus | None = None 

class BookRetrieve(BaseModel):
	id: int
	title: str
	author: str
	total_pages: int | None = None
	status: BookStatus = BookStatus.to_read
	created_at: datetime.date
	class Config:
		from_attributes=True
class ReadingSessionCreate(BaseModel):
	pages_read: int
	date: datetime.date | None = None
	notes: str | None= None

class ReadingSessionUpdate(BaseModel):
	pages_read: int | None= None
	date: datetime.date | None= None
	notes: str | None= None

class ReadingSessionRetrieve(BaseModel):
	id: int
	book_id: int
	pages_read: int 
	date: datetime.date
	notes: str | None= None
	class Config:
		from_attributes=True