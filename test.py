"""
Train:
-train_id PK INT
-name VARCHAR(100)
-available_seats INT
-departure_time DATETIME

Bookings:
-booking_id PK INT
-username VARCHAR(100)
-email VARCHAR(250)
-seats INT
-status ENUM(confirmed, waiting)

WaitingList:
-booking_id FK relates(Bookings)
-train_id FK relates(Train)
-waiting_number INT
"""

# import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect('train_ticket.db')

# # Create a cursor object
# cursor = conn.cursor()

# # Execute a query to get a list of all tables
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# # Fetch all tables
# tables = cursor.fetchall()

# # Print the tables
# for table in tables:
#     print(table[0])

# # Close the cursor and connection
# cursor.close()
# conn.close()


# Hashed Password-------------
from passlib.context import CryptContext

# Initialize passlib's CryptContext with bcrypt scheme
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Define your plain text password
plain_password = "admin"

# Hash the password
hashed_password = pwd_context.hash(plain_password)

# Print the hashed password
print("Hashed Password:", hashed_password)

# Example of verifying a password
is_valid = pwd_context.verify("admin", hashed_password)
print("Is Valid:", is_valid)