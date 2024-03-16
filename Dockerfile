FROM python:3.11.8

WORKDIR /ticketBookingSystem

COPY . /ticketBookingSystem/

RUN pip install -r requirements.txt
