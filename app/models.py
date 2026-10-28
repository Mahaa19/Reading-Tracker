from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Date, Enum as SAEnum, ForeignKey
import datetime, enum

Base = declarative_base()

class BookStatus(str, enum.Enum):
    to_read = "to_read"
    reading = "reading"
    finished = "finished"

class Book(Base):
    
    __tablename__ = "book"

    id = Column(Integer, primary_key =True, index= True) 
    title = Column(String, nullable = False)
    author = Column(String, nullable = False)
    total_pages = Column(Integer, nullable = True)
    created_at = Column(Date, default = datetime.date.today, nullable = False)
    status = Column(SAEnum(BookStatus), default=BookStatus.to_read, nullable=False) 
    sessions = relationship("ReadingSession", back_populates="book",cascade="all, delete-orphan")

class ReadingSession(Base):
    
    __tablename__ = "readingsession"

    id = Column(Integer,primary_key =True, index= True) 
    book_id = Column(Integer,ForeignKey("book.id"), nullable = False)
    pages_read = Column(Integer, nullable = False)
    date = Column(Date, default = datetime.date.today, nullable = False)
    notes = Column(String, nullable = True)
    book = relationship("Book", back_populates="sessions")