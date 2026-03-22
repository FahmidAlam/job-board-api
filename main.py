from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from models import engine, Base, Sessionlocal,Job
from schemas import JobCreate,JobResponse
from fastapi import HTTPException
app = FastAPI()
Base.metadata.create_all(bind = engine)


def get_db():
    db= Sessionlocal()
    try :
        yield db
    finally:
        db.close()

@app.get("/jobs")
def get_jobs(db:Session =Depends(get_db)):
    jobs= db.query(Job).limit(10).all()
    return jobs

# driver for postgresql - psycopg2
@app.post("/jobs",response_model= JobResponse)
def create_job(job:JobCreate,db:Session=Depends(get_db)):
    db_job =Job(**job.dict())
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

@app.delete("/jobs/{job_id}")
def delet_job(job_id: int , db:Session = Depends(get_db)):
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