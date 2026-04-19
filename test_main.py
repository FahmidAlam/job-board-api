#! API endpoint tests — client fixture (from conftest.py) is injected per test, never global
from fastapi.testclient import TestClient
from main import app

#client = TestClient(app)   #! Create a simulated HTTP client that can call FastAPI app directly for testing without running real server


def get_auth_token(client):
    client.post("/register",json={
        "email" : "test@test.com",
        "password":"test12"
    })
    response = client.post("/login",json={
        "email": 'test@test.com',
        "password": "test12"
    })
    return response.json()['access_token']
def auth_headers(client):
    return {'Authorization':f'Bearer {get_auth_token(client)}'}

def test_get_jobs(client):
    response = client.get("/jobs")
    assert response.status_code==200         #! assert - justifies statements durring tests
    assert isinstance(response.json(),list)
    
def test_create_jobs(client):
    job_data={
        'title':'Test Engineer',
        'company':'testcorp',
        'role':'engineer',
        'location':'remote'
    }
    response = client.post("/jobs",json=job_data,headers=auth_headers(client))
    assert response.status_code ==200
    assert response.json()['title'] =='Test Engineer'

def test_get_job_by_id(client):
    job_data={
        'title':'test Engineer',
        'company':"testCorp",
        'role':'engineer',
        'location':'remote'
    }
    headers = auth_headers(client)
    create_response = client.post('/jobs',json=job_data,headers=headers)
    job_id= create_response.json()["id"]
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["id"] ==job_id

def test_delete_job(client):
    job_data={
        'title':'test Engineer',
        'company':"testCorp",
        'role':'engineer',
        'location':'remote'
    }
    headers = auth_headers(client)
    create_response = client.post("/jobs", json=job_data,headers=headers)
    job_id = create_response.json()["id"]
    response = client.delete(f"/jobs/{job_id}")
    assert response.status_code == 204

def test_filter_by_role(client):
    response = client.get("/jobs?role=engineer")
    assert response.status_code == 200
    jobs = response.json()
    for job in jobs:
        assert job["role"] == "engineer"

def test_pagination(client):
    response = client.get("/jobs?limit=5&offset=0")
    assert response.status_code == 200
    assert len(response.json()) <= 5
    
def test_update_job(client):
    job_data={'title':'ML Engineer',
        'company':"testCorp",
        'role':'engineer',
        'location':'remote'
        }
    headers = auth_headers(client)
    create_response = client.post('/jobs',json=job_data,headers=headers)
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

def test_register(client):
    response = client.post("/register", json={
        "email": "newuser@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login(client):
    # Register first
    client.post("/register", json={
        "email": "testuser@example.com",
        "password": "secret123"
    })
    
    # Login
    response = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_job_without_auth(client):
    job_data = {
        "title": "Test Engineer",
        "company": "TestCorp",
        "role": "engineer",
        "location": "remote"
    }
    response = client.post("/jobs", json=job_data)
    assert response.status_code == 401  # Unauthorized

def test_create_job_with_auth(client):
    # Register
    register_response = client.post("/register", json={
        "email": "user@example.com",
        "password": "secret123"
    })
    token = register_response.json()["access_token"]
    
    # Create job with token
    job_data = {
        "title": "Backend Engineer",
        "company": "StartupXYZ",
        "role": "engineer",
        "location": "remote"
    }
    response = client.post(
        "/jobs",
        json=job_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_invalid_password(client):
    client.post("/register", json={
        "email": "user@example.com",
        "password": "secret123"
    })
    
    response = client.post("/login", json={
        "email": "user@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401