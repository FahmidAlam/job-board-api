# Job Board API
   
   A FastAPI backend for a job posting platform.
   
   ## Setup
   
   1. Clone repo
   2. Create virtual env: `python3 -m venv venv && source venv/bin/activate`
   3. Install deps: `pip install -r requirements.txt`
   4. Create database: `createdb job_board_dev`
   5. Run: `uvicorn main:app --reload`
   
   ## Endpoints
   
   - GET /jobs — list all jobs
   - GET /jobs/{id} — get job by id
   - POST /jobs — create job
   - PUT /jobs/{id} — update job
   - DELETE /jobs/{id} — delete job