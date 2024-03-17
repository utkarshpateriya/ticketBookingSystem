from pydantic import BaseModel
from datetime import datetime

class Train(BaseModel):
    train_name: str
    total_seats: int

class Booking(BaseModel):
    train_id: int
    user_email: str
    seat_number: int = None
    
class TrainCreate(BaseModel):
    name: str
    seats: int
    departure_time: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Doronto Express",
                "available_seats": 100,
                "departure_time": "2024-03-20T10:00:00"
            }
        }
        
class BookingSeats(BaseModel):
    username: str
    email: str
    number_of_seats: int
    train_id: int