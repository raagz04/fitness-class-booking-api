
from datetime import datetime, timedelta
from utils import ist_to_utc
from models import FitnessClass

def seed_data(db_session):
    if db_session.query(FitnessClass).count() > 0:
        return

    now = datetime.now()
    classes = [
        ("Yoga", "Keneshia", datetime(now.year, now.month, now.day, 7, 0) + timedelta(days=1), 3),
        ("Zumba", "Guru", datetime(now.year, now.month, now.day, 18, 0) + timedelta(days=1), 4),
        ("HIIT", "Rishi", datetime(now.year, now.month, now.day, 7, 0) + timedelta(days=2), 2),
        ("Yoga", "Ridhi", datetime(now.year, now.month, now.day, 18, 0) + timedelta(days=2), 2),
    ]

    for name, instructor, start_ist, capacity in classes:
        cls = FitnessClass(
            name=name,
            instructor=instructor,
            date_time=ist_to_utc(start_ist),
            capacity=capacity
        )
        db_session.add(cls)
    db_session.commit()
