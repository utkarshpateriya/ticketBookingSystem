# Train Ticket Booking System

This is a backend system for a train ticket booking system implemented using FastAPI, SQLite, and SQLAlchemy.

## Setup and Installation

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/train-ticket-booking-system.git
    ```

2. Navigate to the project directory:

    ```bash
    cd train-ticket-booking-system
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    # On Unix/macOS
    python3 -m venv env
    
    # On Windows
    python -m venv env
    ```

4. Activate the virtual environment:

    ```bash
    # On Unix/macOS
    source env/bin/activate
    
    # On Windows
    .\env\Scripts\activate
    ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

7. You can now access the FastAPI documentation at `http://localhost:8000/docs` and test the API endpoints using the interactive documentation.

## API Endpoints

### Create Train
- **URL:** `/trains/`
- **Method:** `POST`
- **Description:** Create a new train with a name and number of seats.
- **Request Body:**
  ```json
  {
      "name": "Express 123",
      "seats": 100
  }
