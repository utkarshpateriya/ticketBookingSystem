from fastapi import FastAPI
import sqlite3
from routers.booking import router

app = FastAPI()
app.include_router(router)

conn = sqlite3.connect('ticket_booking.db', check_same_thread=False)
c = conn.cursor()

# Create tables if not exist
c.execute('''CREATE TABLE IF NOT EXISTS trains
             (train_id INTEGER PRIMARY KEY AUTOINCREMENT,
              train_name TEXT NOT NULL,
              total_seats INTEGER NOT NULL,
              available_seats INTEGER NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS bookings
             (booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
              train_id INTEGER NOT NULL,
              user_email TEXT NOT NULL,
              seat_number INTEGER NOT NULL,
              status TEXT NOT NULL,
              booked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY(train_id) REFERENCES trains(train_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS waiting_list
             (waiting_id INTEGER PRIMARY KEY AUTOINCREMENT,
              train_id INTEGER NOT NULL,
              user_email TEXT NOT NULL,
              status TEXT NOT NULL,
              waiting_at DATETIME DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY(train_id) REFERENCES trains(train_id))''')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)