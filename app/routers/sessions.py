from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.models import Book as BookModel
from app.database import get_db
from app.schemas import ReadingSessionCreate,ReadingSessionRetrieve,ReadingSessionUpdate
from app.models import ReadingSession as SessionModel

router = APIRouter(prefix="/books/{book_id}/sessions", tags=["sessions"])

def get_book_or_404(book_id: int, db: Session) -> BookModel:
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/", response_model=list[ReadingSessionRetrieve])
def list_session(book_id: int, db: Session = Depends(get_db)):
    get_book_or_404(book_id, db)
    db_session = db.query(SessionModel).filter(SessionModel.book_id == book_id).all()
    return db_session

@router.post("/",response_model=ReadingSessionRetrieve, status_code=201)
def create_session(book_id: int, session: ReadingSessionCreate, db: Session = Depends(get_db) ):
    get_book_or_404(book_id, db)
    db_session = SessionModel(book_id=book_id, **session.model_dump(exclude_unset=True))
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session
