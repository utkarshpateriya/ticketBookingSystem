from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.trainSchema import Train, Booking
from utils.bookingUtils import send_email, send_reminder
import sqlite3

conn = sqlite3.connect('ticket_booking.db', check_same_thread=False)
c = conn.cursor()

router = APIRouter()

@router.get('/')
def index():
    return {
        "details":"Working"
    }
    
@router.post('/add_train')
def add_train(train: Train):
    c.execute('''INSERT INTO trains (train_name, total_seats, available_seats) VALUES (?, ?, ?)''', (train.train_name, train.total_seats, train.total_seats))
    conn.commit()
    return {'message': 'Train added successfully'}

@router.get('/view_trains')
def view_trains():
    c.execute('''SELECT * FROM trains''')
    trains = c.fetchall()
    train_list = []
    for train in trains:
        train_list.append({
            'train_id': train[0],
            'train_name': train[1],
            'available_seats': train[3]
        })
    return train_list

@router.post('/book_ticket')
def book_ticket(booking: Booking, background_tasks: BackgroundTasks):
    c.execute('''SELECT available_seats FROM trains WHERE train_id = ?''', (booking.train_id,))
    available_seats = c.fetchone()[0]

    if available_seats > 0:
        if booking.seat_number:
            c.execute('''INSERT INTO bookings (train_id, user_email, seat_number, status) VALUES (?, ?, ?, ?)''', (booking.train_id, booking.user_email, booking.seat_number, 'Confirmed'))
        else:
            c.execute('''INSERT INTO bookings (train_id, user_email, status) VALUES (?, ?, ?)''', (booking.train_id, booking.user_email, 'Confirmed'))
        c.execute('''UPDATE trains SET available_seats = available_seats - 1 WHERE train_id = ?''', (booking.train_id,))
        conn.commit()
        background_tasks.add_task(send_reminder, booking.train_id)
        return {'message': 'Ticket booked successfully'}
    else:
        c.execute('''SELECT COUNT(*) FROM waiting_list WHERE train_id = ?''', (booking.train_id,))
        waiting_count = c.fetchone()[0]
        c.execute('''INSERT INTO waiting_list (train_id, user_email, status) VALUES (?, ?, ?)''', (booking.train_id, booking.user_email, 'Waiting'))
        conn.commit()
        return {'message': f'Ticket added to waiting list. You are at position {waiting_count+1}'}

@router.post('/cancel_ticket')
def cancel_ticket(booking_id: int):
    c.execute('''SELECT * FROM bookings WHERE booking_id = ?''', (booking_id,))
    booking = c.fetchone()
    if booking:
        c.execute('''DELETE FROM bookings WHERE booking_id = ?''', (booking_id,))
        c.execute('''UPDATE trains SET available_seats = available_seats + 1 WHERE train_id = ?''', (booking[1],))
        conn.commit()
        # Check waiting list and confirm the first in queue
        c.execute('''SELECT * FROM waiting_list WHERE train_id = ? AND status = 'Waiting' ORDER BY waiting_at''', (booking[1],))
        waiting = c.fetchone()
        if waiting:
            c.execute('''INSERT INTO bookings (train_id, user_email, status) VALUES (?, ?, ?)''', (waiting[1], waiting[2], 'Confirmed'))
            c.execute('''DELETE FROM waiting_list WHERE waiting_id = ?''', (waiting[0],))
            conn.commit()
            # Send email to the newly confirmed passenger
            send_email(waiting[2], "Congratulations! Your Ticket is Confirmed", f"Dear Passenger, Your seat number is {booking[3]}")
        return {'message': 'Ticket canceled successfully'}
    else:
        raise HTTPException(status_code=404, detail='Invalid booking ID')