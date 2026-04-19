from passlib.context import CryptContext    #!CryptContext — passlib's main object for hashing.
from datetime import datetime , timedelta    #! timedelta - set token expiry
from jose import JWTError , jwt
from fastapi import HTTPException, status,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from database import get_db
from models import User
from typing import Optional
load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")
SECRET_KEY = os.getenv("SECRET_KEY")  #! used to sign JWT
ALGORITHM = 'HS256'                 #! HS256 → hashing algorithm for JWT
security = HTTPBearer()      #! HTTPBearer - extract token from Authorization header automatically ,doesn't verify the token


def hash_password(password: str) ->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hased_password:str)->bool :
    return pwd_context.verify(plain_password,hased_password)

def create_access_token(data:dict , expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db:Session = Depends(get_db)):
    token = credentials.credentials  #!From header- Authorization: Bearer <token>
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email :str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401,detail = "Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email==email).first()
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    return user 