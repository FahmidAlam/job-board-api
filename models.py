from sqlalchemy import Column,Integer,String, DateTime,Float,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
DATABASE_URL = "postgresql://postgres:DoomVLoki@localhost:5432/job_board_dev"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(autocommit = False , autoflush = False,bind = engine)
Base = declarative_base()
class Job(Base):
    __tablename__ ='jobs'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False) 
    location = Column(String, nullable=False)  
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow) 