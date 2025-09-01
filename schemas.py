from pydantic import BaseModel, EmailStr, Field
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)   
    email: EmailStr                                    
    password: constr(min_length=6)                    

class ClassOut(BaseModel):
    id: int
    name: str
    instructor: str
    start_time: str 
    timezone: str
    capacity: int
    available_slots: int

class BookIn(BaseModel):
    class_id: int = Field(..., gt=0)
    client_name: str = Field(..., min_length=1, max_length=120)
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    created_at: str
    class_name: str
    instructor: str
    start_time: str
    timezone: str
