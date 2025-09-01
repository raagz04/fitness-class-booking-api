# RAAGAVI FITNESS STUDIO BOOKING API

This project is a simple backend API for a fictional fitness studio. The goal is to allow clients to view available classes, register as users, and book a spot in their preferred fitness session.

The API is built using FastAPI with SQLite as the database and includes proper timezone handling (IST to user’s timezone).

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite)


## Features

User registration with validation (name, email, password).

View available fitness classes (Yoga, Zumba, HIIT, etc.).

Book a class with real-time slot availability check.

View all bookings for a given user (by email).

Timezone conversion support (classes are stored in IST, but can be shown in user’s local timezone).

Error handling for missing fields, overbooking, invalid emails, etc.

##Tech Stack

Backend: FastAPI (Python)

Database: SQLite (in-memory/file-based)

Timezone: pytz and datetime for conversions

## Validation: Pydantic models

### Project Structure
 main.py         # Entry point for FastAPI app
 models.py       # Database models (Users, Classes, Bookings)
 schemas.py      # Pydantic schemas for request/response validation
 utils.py        # Helper functions (timezone conversion, validators)
 emailer.py      # Utility for sending email notifications
 seed.py         # Script tfor already having initial data (classes, users, etc.)
 booking.db      # SQLite database 
 requirements.txt # Python dependencies
 README.md       # Project documentation


## Setup Instructions

Clone the repository

git clone https://github.com/raagz04/fitness-class-booking-api.git
cd fitness-booking-api


## Created and activated a virtual environment

python -m venv fitness
.\fitness\Scripts\activate

## Required dependencies to install

pip install -r requirements.txt

## Command To Run the FastAPI app

uvicorn main:app --reload

The server will start at: http://127.0.0.1:8000  
Interactive API docs (Swagger UI) available at: http://127.0.0.1:8000/docs

## API Endpoints

1. To register a User
POST /users

Request Body:

{
  "name": "Raagavi",
  "email": "raagavi@fitness.com",
  "password": "raagzz"
}


Validation Done:

All fields required
Email must be valid format
Password should contain atleast 6 characters

2. To get Available Classes

GET /classes

Returns list of upcoming fitness classes with slots, instructor, and time.

3. To book a Class

POST /book

Request Body:

{
  "class_id": 1,
  "client_email": "raagavi@fitness.com"
}

Checks availability

Reduces available slots if successfull

4. To get User Bookings

GET /bookings?email=raagavi@fitness.com

Returns all bookings for the given email.

## Seed Data

By default, the database is seeded with a few sample classes (Yoga, Zumba, HIIT) so that you can start testing immediately.

If you want to reset the database, just delete booking.db and rerun the app — it will regenerate with fresh sample data.

Example cURL Requests
### Create user
curl -X POST "http://127.0.0.1:8000/users" -H "Content-Type: application/json" -d '{"name":"John","email":"john@example.com","password":"test123"}'

### Get classes
curl -X GET "http://127.0.0.1:8000/classes"

### Book class
curl -X POST "http://127.0.0.1:8000/book" -H "Content-Type: application/json" -d '{"class_id":1,"client_email":"john@example.com"}'

### Get bookings
curl -X GET "http://127.0.0.1:8000/bookings?email=john@example.com"

## Loom Video

A walkthrough video is included demonstrating:

-User creation
-Timezone handling
-Booking a class
-Error handling (invalid inputs, overbooking, etc.)

## Extra Features Implemented

Input validation with Pydantic
Email format checking
Automatic database seeding
Timezone conversion logic