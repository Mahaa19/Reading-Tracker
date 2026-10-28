from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal, engine
from app.routers import books, sessions
from app.models import Base as Basemodel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods = ["*"]
)
Basemodel.metadata.create_all(bind=engine)

app.include_router(books.router)
app.include_router(sessions.router)

@app.get("/")
def greet ():
    return "Whatzzup!"
