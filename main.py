from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from api.login.login import Login
from api.util.jwt import jwt
from api.util.jwt import *
from api.user.user import User
from typing import Annotated

app = FastAPI()

# CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# origins
origins = [
    "*",
    # "http://localhost",
    # "http://localhost:8080",
]

class TokenSchema(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str

class LoginInput(BaseModel):
    id:str
    password:str
@app.post("/login", summary="Create access and refresh tokens for user", response_model=TokenSchema)
def login(input:LoginInput):
    login = Login()

    login.id = input.id
    login.password = input.password
    result = login.login()

    if result is None:
        raise HTTPException(status_code=404, detail="Invalid ID or password")
    # 디비에 있는 해쉬한 패스워드도 비교해야 함

    token = {
        "token_type": "bearer",
        "access_token": create_access_token(input.id),
        "refresh_token": create_refresh_token(input.id),
    }

    return token



    # sql = "SELECT * FROM user"
    # cursor.execute(sql)

    # columns = [desc[0] for desc in cursor.description]
    # result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    return result

@app.get("/check/id/{id}")
def check_id(id: str):
    login = Login()

    login.id = id
    return login.check_id()

@app.get("/test/{value}")
def test(value: str):
    user = User()

    user.id = value
    return user.get_user_info_by_id()
