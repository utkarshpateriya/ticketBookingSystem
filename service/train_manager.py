from database import SessionLocal
from models.booking_model import Train, WaitingList, Booking, BookingStatus
from schemas.trainSchema import BookingSeats
from utils.authentication import AdminAuthentication
from sqlalchemy.orm import Session
import uuid

admin_authentication = AdminAuthentication()

class TrainManager:
    
    def create_train(self, train_data: Train):
        db = SessionLocal()
        train = Train(**train_data.dict())
        db.add(train)
        db.commit()
        db.refresh(train)
        return {"message": "Train created successfully"}
    
    def list_trains(self, db):
        trains = db.query(Train).all()
        train_data = []

        for train in trains:
            # available seats
            booked_seats = db.query(Booking).filter(Booking.train_id == train.train_id, Booking.status == BookingStatus.confirmed).count()
            available_seats = train.seats - booked_seats

            # waiting list count
            waiting_list_count = db.query(WaitingList).filter(WaitingList.train_id == train.train_id).count()

            train_status = {
                "train_id": train.train_id,
                "name": train.name,
                "available_seats": available_seats,
                "waiting_list_count": waiting_list_count
            }
            train_data.append(train_status)

        return train_data
    
    def book_seats(self, booking_data: BookingSeats, db: Session):
        # Retrieve train details
        train = db.query(Train).filter(Train.train_id == booking_data.train_id).first()
        if not train:
            return {"error": "Train not found"}

        # Calculate available seats
        booked_seats = db.query(Booking).filter(Booking.train_id == booking_data.train_id, Booking.status == BookingStatus.confirmed).count()
        available_seats = train.seats - booked_seats

        # Check if there are available seats
        if available_seats >= booking_data.number_of_seats:
            # Create a new booking
            booking_id = str(uuid.uuid4())
            booking = Booking(
                booking_id=booking_id,
                username=booking_data.username,
                email=booking_data.email,
                seats=booking_data.number_of_seats,
                status=BookingStatus.confirmed,
                train_id=booking_data.train_id
            )
            db.add(booking)
            db.commit()

            return {"message": "Booking confirmed"}

        else:
            # Add to waiting list
            max_waiting_number = db.query(WaitingList).filter(WaitingList.train_id == booking_data.train_id).order_by(WaitingList.waiting_number.desc()).first()
            next_waiting_number = (max_waiting_number.waiting_number + 1) if max_waiting_number else 1
            
            waiting_booking = WaitingList(
                booking_id=None,  # No booking ID yet, will be updated later
                train_id=booking_data.train_id,
                waiting_number=next_waiting_number
            )
            db.add(waiting_booking)
            db.commit()

            return {"message": "Added to waiting list", "waiting_number": next_waiting_number}
