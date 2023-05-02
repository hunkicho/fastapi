from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from api.login.login import Login
from api.util.jwt import jwt
from api.util.jwt import *

app = FastAPI()

class User(BaseModel):
    id:str
    password:str
@app.post("/login", summary="Create access and refresh tokens for user")
def login(user:User):
    login = Login()

    login.id = user.id
    login.password = user.password
    result = login.login()
    print(result)

    if result is None:
        raise HTTPException(status_code=404, detail="Invalid ID or password")
    # 디비에 있는 해쉬한 패스워드도 비교해야 함

    token = {
        "token_type": "bearer",
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
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