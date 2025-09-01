import logging
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas import UserCreate
from database import engine, SessionLocal, Base, get_db
import models, schemas, utils, seed, emailer
from fastapi import Body

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Raagavi Fitness Class Booking API")

#table creation
Base.metadata.create_all(bind=engine)

@app.post("/users", status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Checking if email already exists
    existing = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered.")
    
    user = models.User(
        name=payload.name,
        email=payload.email.lower(),
        password=payload.password 
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "email": user.email}

@app.on_event("startup")
def startup():
    """Seed the DB with sample classes if not already present"""
    db = SessionLocal()
    try:
        seed.seed_data(db)
        logger.info("Seeded classes (if not already present).")
    finally:
        db.close()

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}


@app.get("/classes", response_model=list[schemas.ClassOut])
def get_classes(
    tz: str | None = Query(default="Asia/Kolkata"),
    db: Session = Depends(get_db)
):
    """List all classes with available slots"""
    tz = utils.ensure_tz_name(tz)
    classes = db.query(models.FitnessClass).order_by(models.FitnessClass.date_time).all()

    out = []
    for c in classes:
        booked = db.query(models.Booking).filter(models.Booking.class_id == c.id).count()
        available = c.capacity - booked
        out.append(schemas.ClassOut(
            id=c.id,
            name=c.name,
            instructor=c.instructor,
            start_time=c.date_time.isoformat() + "Z", 
            timezone=tz,
            capacity=c.capacity,
            available_slots=available
        ))
    return out


@app.post("/book", response_model=schemas.BookingOut, status_code=201)
def book_class(
    payload: schemas.BookIn,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Book a slot for a class"""
    #To Check if class exists
    c = db.query(models.FitnessClass).filter(models.FitnessClass.id == payload.class_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Class not found.")

    #Checking availability
    booked_count = db.query(models.Booking).filter(models.Booking.class_id == c.id).count()
    if c.capacity - booked_count <= 0:
        raise HTTPException(status_code=409, detail="No slots available for this class.")

    #Prevent duplicate booking for same email
    existing = db.query(models.Booking).filter(
        models.Booking.class_id == c.id,
        models.Booking.client_email == payload.client_email.lower()
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="You have already booked this class with this email.")

    #Create booking
    booking = models.Booking(
        class_id=payload.class_id,
        client_name=payload.client_name.strip(),
        client_email=payload.client_email.lower(),
        booked_at=datetime.utcnow()
    )
    db.add(booking)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Booking conflict (duplicate).")
    db.refresh(booking)

    #Scheduling email notification in background
    try:
        local_time = utils.utc_iso_to_tz(c.date_time, "Asia/Kolkata")
    except Exception:
        local_time = c.date_time

    subject = f"Booking Confirmed: {c.name}"
    body = (
        f"Hi {booking.client_name},\n\n"
        f"Your booking is confirmed.\n\n"
        f"Class: {c.name}\n"
        f"Instructor: {c.instructor}\n"
        f"Start (IST): {local_time}\n\n"
        "See you there!\n Raagavi Fitness Studio"
    )
    background_tasks.add_task(emailer.send_email, booking.client_email, subject, body)

    return schemas.BookingOut(
        id=booking.id,
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email,
        created_at=booking.booked_at.isoformat() + "Z", 
        class_name=c.name,
        instructor=c.instructor,
        start_time=c.date_time.isoformat() + "Z",      
        timezone="UTC"
    )


@app.get("/bookings", response_model=list[schemas.BookingOut])
def get_bookings(
    email: str = Query(..., description="Email address used for bookings"),
    tz: str | None = Query(default="Asia/Kolkata"),
    db: Session = Depends(get_db)
):
    """Get all bookings for a given email"""
    tz = utils.ensure_tz_name(tz)
    rows = (
        db.query(models.Booking, models.FitnessClass)
        .join(models.FitnessClass, models.Booking.class_id == models.FitnessClass.id)
        .filter(models.Booking.client_email == email.lower())
        .order_by(models.FitnessClass.date_time)
        .all()
    )

    out = []
    for b, c in rows:
        out.append(schemas.BookingOut(
            id=b.id,
            class_id=b.class_id,
            client_name=b.client_name,
            client_email=b.client_email,
            created_at=b.booked_at.isoformat() + "Z",  
            class_name=c.name,
            instructor=c.instructor,
            start_time=c.date_time.isoformat() + "Z", 
            timezone=tz
        ))
    return out
