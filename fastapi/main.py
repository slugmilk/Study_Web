from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

users = {
    0: {"userid": "apple", "name": "김사과"},
    1: {"userid": "banna", "name": "반하나"},
    2: {"userid": "orange", "name": "오렌지"}
}

# http://127.0.0.1:8000
@app.get("/")
async def root():
    return {"message": "Hello FastAPI!"}

# http://127.0.0.1:8000/users/id
@app.get("/users/{id}")
def find_user(id: int):
    user = users[id]
    return user

# http://127.0.0.1:8000/users/0/userid
# http://127.0.0.1:8000/docs
@app.get("/users/{id}/{key}")
def find_user_by_key(id: int, key: str):
    user = users[id][key]
    return user

# http://127.0.0.1:8000/users/id-by-name?name=김사과
#@app.get("/users/id-by-name")
#async def find_user_by_name(name: str):
#    for userid, user in users.items():
#        if user['name'] == name:
#           return user
#   return {"error": "데이터를 찾지 못함"}

class User(BaseModel):
    userid: str
    name: str

# http://127.0.0.1:8000/users/0
@app.post("/users/{id}")
async def create_user(id: int, user: User):
    if id in users:
        return {"error": "이미 존재하는 키"}
    users[id] = user.__dict__
    return {"success": "ok"}

class UserForUpdate(BaseModel):
    userid: Optional[str]
    name: Optional[str]

@app.put("/users/{id}")
async def update_user(id: int, user: UserForUpdate):
    if id not in users:
        return {"error": "id가 존재하지 않음"}

    if user.userid:
        users[id]['userid'] = user.userid

    if user.name:
        user[id]['name'] = user.name

    return {"success": "ok"}

@app.delete("/users/{id}")
def delete_item(id: int):
    users.pop(id)
    return {"success": "ok"}
