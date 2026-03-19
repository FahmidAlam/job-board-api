from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class JobCreate(BaseModel):
    title : str
    company : str
    role : str
    location: str
    salary_min:Optional[float] =None
    salary_max:Optional[float]= None
    
class JobResponse(BaseModel):
    id:int
    title:str
    company:str
    role:str
    location: str
    created_at:datetime
    class Config:
        from_attribute =True

