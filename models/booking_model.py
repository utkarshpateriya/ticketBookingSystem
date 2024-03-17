from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base

class Train(Base):
    __tablename__ = "trains"

    train_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    seats = Column(Integer)
    departure_time = Column(DateTime)
    
    class Config:
        orm_mode = True
    
class BookingStatus(PyEnum):
    confirmed = "confirmed"
    waiting = "waiting"
    
class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.train_id"), primary_key=True)
    username = Column(String(100))
    email = Column(String(250))
    seats = Column(Integer)
    status = Column(Enum(BookingStatus))
    
class WaitingList(Base):
    __tablename__ = "waiting_list"

    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.train_id"), primary_key=True)
    waiting_number = Column(Integer)