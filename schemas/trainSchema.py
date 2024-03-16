from pydantic import BaseModel
from typing import Optional

class Train(BaseModel):
    train_name: str
    total_seats: int

class Booking(BaseModel):
    train_id: int
    user_email: str
    seat_number: int = None