'''
    - Pydantic schemas define the validated input/output structure of API data
    - schemas manage how data enters and leaves the application safely
'''

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
class JobCreate(BaseModel):
    title : str
    company : str
    role : str
    location: str
    salary_min:float |None= None
    salary_max:Optional[float]= None
    
class JobResponse(BaseModel):
    id:int
    title:str
    company:str
    role:str
    location: str
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id : int
    email: str
    created_at : datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token : str
    token_type: str
