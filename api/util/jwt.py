from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, Union
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError
from api.user.user import User

ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # should be kept secret
JWT_REFRESH_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

def get_hashed_password(password: str) -> str:
    """해시를 적용한 password return"""
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """일반password와 해시를 적용한 password 일치여부 return """
    return password_context.verify(password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)

    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        token_data = {"user_id", user_id}
        print(token_data)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=401, detail="Token expired", headers={"WWW-Authenticate": "Bearer"},)
    except JWTError:
        raise credentials_exception

    user = User()
    user.id = token_data["user_id"]
    user_info = user.get_user_info_by_id()

    if user_info is None:
        raise credentials_exception
    return user_info

async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user