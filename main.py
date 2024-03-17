from fastapi import FastAPI
from routers.booking import router
from models.booking_model import Train, Booking, WaitingList
from database import engine, Base

app = FastAPI()
app.include_router(router)

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)