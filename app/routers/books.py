from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book as BookModel
from app.schemas import BookCreate, BookRetrieve, BookUpdate


router = APIRouter(prefix="/books", tags=["books"])
@router.get("/", response_model = list[BookRetrieve])
def list_books(db: Session = Depends(get_db)):
    db_book = db.query(BookModel).all()
    return db_book

@router.get("/{id}", response_model = BookRetrieve)
def get_book(id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == id).first()
    if db_book:
        return db_book
    else:
        raise HTTPException(status_code=404, detail="Book not found")
    
@router.post("/",response_model = BookRetrieve, status_code = 201)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookModel(**book.model_dump(exclude_unset=True)) #instead of app.models.Book
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return {"detail": "Book is deleted"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@router.patch("/{id}",response_model = BookRetrieve)
def update_book(id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == id).first()
    if db_book:
        update_data = book.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book
    else:
        raise HTTPException(status_code=404, detail="Book not found")
