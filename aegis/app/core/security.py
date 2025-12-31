from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta 
from app.core.config import settings 

pwd_context=CryptContext(schemes=[settings.PASSWORD_HASH_SCHEME],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_passoword(password:str, hashed:str)->bool:
    return pwd_context.verify(password, hashed)

def _create_token(subject:str,token_type:str,expires_delta):
    payload={
        "sub":subject,
        "type": token_type,
        "exp":datetime.utcnow()+expires_delta,
        "iat":datetime.utcnow(),

    }
    return jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALOGRITHM)

def create_access_token(user_id:str)->str:
    return _create_token(
        user_id,
        "access",
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
def create_refresh_token(user_id:str)->str:
    return _create_token(user_id, "refresh", timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),)


