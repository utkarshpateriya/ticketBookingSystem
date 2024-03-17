from fastapi import APIRouter, Depends
from utils.authentication import AdminAuthentication
from service.train_manager import TrainManager
from schemas.trainSchema import TrainCreate, BookingSeats
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal
from models.booking_model import Train

train = TrainManager()
admin_authentication = AdminAuthentication()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get('/')
def index():
    return {
        "details":"Working"
    }
    
@router.post("/create-train/")
def post_train(train_data: TrainCreate, authenticated: bool = Depends(admin_authentication.authenticate_user)):
    return train.create_train(train_data)

@router.get("/trains")
def list_trains(db: Session = Depends(get_db)):
    return train.list_trains(db)

@router.post("/book-seats")
def book_seat(booking_seats: BookingSeats, db: Session = Depends(get_db)):
    return train.book_seats(booking_data=booking_seats, db=db)