from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def read_root():
    return {'status':"API running"}
@app.get('/jobs')
def get_jobs():
    return [
        {"id": 1, "title": "Backend Engineer", "company": "StartupXYZ"},
        {"id": 2, "title": "ML Engineer", "company": "TechCorp"}
    ]
