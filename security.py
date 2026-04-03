from passlib.context import CryptContext
from datetime import datetime , timedelta
from jose import JWTError , jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'


def hash_password(password: str) ->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hased_password:str)->bool :
    return pwd_context.verify(plain_password,hased_password)

def create_access_token(data:dict , expires_delta: timedelta =None |None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM=ALGORITHM)
    return encoded_jwt