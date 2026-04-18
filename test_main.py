from fastapi.testclient import TestClient
from main import app

client = TestClient(app)   #! Create a simulated HTTP client that can call FastAPI app directly for testing without running real server


def get_auth_token():
    client.post("/register",json={
        "email" : "test@test.com",
        "password":"test12"
    })
    response = client.post("/login",json={
        "email": 'test@test.com',
        "password": "test12"
    })
    return response.json()['access_token']
def auth_headers():
    return {'Authorization':f'Bearer {get_auth_token()}'}

def test_get_jobs():
    response = client.get("/jobs")
    assert response.status_code==200         #! assert - justifies statements durring tests
    assert isinstance(response.json(),list)
    
def test_create_jobs():
    job_data={
        'title':'Test Engineer',
        'company':'testcorp',
        'role':'engineer',
        'location':'remote'
    }
    response = client.post("/jobs",json=job_data,headers=auth_headers())
    assert response.status_code ==200
    assert response.json()['title'] =='Test Engineer'

def test_get_job_by_id():
    job_data={
        'title':'test Engineer',
        'company':"testCorp",
        'role':'engineer',
        'location':'remote'
    }
    create_response = client.post('/jobs',json=job_data,headers=auth_headers())
    job_id= create_response.json()["id"]
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["id"] ==job_id

def test_delete_job():
    job_data={
        'title':'test Engineer',
        'company':"testCorp",
        'role':'engineer',
        'location':'remote'
    }
    create_response = client.post("/jobs", json=job_data,headers=auth_headers())
    job_id = create_response.json()["id"]
    response = client.delete(f"/jobs/{job_id}")
    assert response.status_code == 204

def test_filter_by_role():
    response = client.get("/jobs?role=engineer")
    assert response.status_code == 200
    jobs = response.json()
    for job in jobs:
        assert job["role"] == "engineer"

def test_pagination():
    response = client.get("/jobs?limit=5&offset=0")
    assert response.status_code == 200
    assert len(response.json()) <= 5
    
def test_update_job():
    job_data={'title':'ML Engineer',
        'company':"testCorp",
        'role':'engineer',
        'location':'remote'}
    create_response = client.post('/jobs',json=job_data,headers=auth_headers())
    job_id = create_response.json()["id"] 
    updated_data={
        'title': 'backend engineer',
        'company':"testCorp",
        'role':'engineer',
        'location':'remote'
    }
    response = client.put(f"/jobs/{job_id}",json=updated_data)
    assert response.status_code ==200
    assert response.json()['title'] == 'backend engineer'