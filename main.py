'''
This file handles Authentication & Security:
    * Hashing passwords → so raw passwords are never stored
    * Verifying passwords → during login
    * Creating JWT tokens → after login
    * Validating JWT tokens → for protected routes
    * Getting current user → from token
'''
import logging        #! logging: recording what different program is doing (with levels) so we can debug, monitor, and track it later.
from fastapi import Depends, FastAPI,HTTPException,status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from models import engine, Base, Sessionlocal,Job,User
from schemas import JobCreate,JobResponse, UserCreate, Token
from database import get_db
from typing import Optional,Annotated
from security import hash_password, create_access_token, verify_password,get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
Base.metadata.create_all(bind = engine)   #! Scans all SQLAlchemy models linked to Base and creates their corresponding tables in the database connected through engine if those tables do not already exist.

db_dependency= Annotated[Session,Depends(get_db)] 

@app.exception_handler(RequestValidationError)    #! @app.exception_handler(X) means: "whenever error of type X bubbles up anywhere in the app, run this function instead of crashing."
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "detail":"Invalid request",
            "errors": exc.errors()
        }
    )

@app.get("/jobs",response_model=list[JobResponse])
def get_jobs(role: Optional[str]=None,
            location: Optional[str]=None,
            salary_min:Optional[float]=None,
            salary_max:Optional[float]=None,
            limit:int =10,
            offset:int=0,
            db:Session=Depends(get_db)
            ):
    query = db.query(Job)
    if role:
        query = query.filter(Job.role==role)
    if location:
        query = query.filter(Job.location==location)
    if  salary_min:
        query= query.filter(Job.salary_min>=salary_min)
    if  salary_max:
        query= query.filter(Job.salary_max<=salary_max)
    return query.limit(limit).offset(offset).all()

#** driver for postgresql - psycopg2
@app.post("/jobs",response_model= JobResponse)
def create_job(job:JobCreate,
                current_user:User=Depends(get_current_user),
                db:Session=Depends(get_db)
                ):
    logger.info(f"User {current_user.email} creating job: {job.title}")
    db_job =Job(**job.dict(),user_id =current_user.id)   #! here the API data  job(which is a schema "JobCreate") becomes DB object Job(it's a DB table)
    #! used "**" to unpack the dictonary into named fields as SQLAlchemy model constructor deosn't expect /support a raw dictonary object
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/{job_id}",response_model=JobResponse)
def get_job(job_id:int,db:Session=Depends(get_db)):
    job =db.query(Job).filter(Job.id==job_id).first()
    if not job:
        raise HTTPException(status_code=404,detail="job not found")
    return job

@app.delete("/jobs/{job_id}",status_code=204)
def delete_job(job_id: int , db:Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id==job_id).first()
    if not job:
        raise HTTPException(status_code=404,detail="job not found")
    db.delete(job)
    db.commit()
    

@app.put("/jobs/{job_id}",response_model=JobResponse)
def update_job(job_id: int,job_update:JobCreate, db:Session=Depends(get_db)):
    job=db.query(Job).filter(Job.id==job_id).first()
    if not job: 
        raise HTTPException(status_code=404, detail="Job not found")
    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(job,key,value)
    db.commit()
    db.refresh(job)
    return job

@app.post("/register",response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email==user.email).first()
    if existing :
        raise HTTPException(status_code=409,detail="Email already registered")
    hashed_pw = hash_password(user.password)
    new_user = User(email =user.email,hashed_password= hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={'sub':new_user.email})
    return {'access_token': access_token,'token_type':"bearer"}

@app.post("/login",response_model = Token)
#def login(email:str,password:str,db:Session = Depends(get_db)):
def login(credentials: UserCreate,db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email==credentials.email).first()
    if not user or not verify_password(credentials.password,user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invaid credential"
        )
    access_token = create_access_token(data={"sub":user.email})
    return {'access_token':access_token,'token_type':"bearer"}
