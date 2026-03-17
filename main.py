from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from models import engine, Base, Sessionlocal,Job
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
