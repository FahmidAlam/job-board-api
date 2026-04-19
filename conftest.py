'''
    pytest test infrastructure: routes DB to SQLite, shares one connection per test, rolls back after each test
    the file name conftest.py is hardcoded in pytest's discovery logic.
    It's  pytest's automatically loaded configuration file, triggered purely by its name, nothing else.
'''
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db
from models import Base

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield                                   #! yield = “run tests now, then come back and clean everything”
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    # one connection shared across ALL requests in this test
    connection = engine.connect()   #! connection : the actual wire of the database
    transaction = connection.begin() #! transaction:  A checkpoint — all writes since begin() can be undone

    def override_get_db():
        session = TestingSession(bind=connection)   #! session: SQLAlchemy's unit of work - tracks object, build queries
        try:
            yield session
        finally:
            # close session but NOT the connection
            session.close()   

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    transaction.rollback()    # undo everything after the test
    connection.close()