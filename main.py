from fastapi import FastAPI, Header
from pydantic import BaseModel

api = FastAPI(title = "My API", description = "My API description", version = "1.0.0", openapi_tags=[
        {
        'name': 'home',
        'description': 'default functions'
    },
    {
        'name': 'items',
        'description': 'functions that are used to deal with items'
    }
])

users_db = [
    {
        'user_id': 1,
        'name': 'Alice',
        'subscription': 'free tier'
    },
    {
        'user_id': 2,
        'name': 'Bob',
        'subscription': 'premium tier'
    },
    {
        'user_id': 3,
        'name': 'Clementine',
        'subscription': 'free tier'
    }
]


@api.get("/",
         name="Hellow World", 
         tags=['home'])
def greatings():
    "Returns an Hello word"
    return "Bienvenu à mon API"


@api.get("/users", tags=['home', 'items'])
def get_all_users() -> list[dict]:
    return users_db

@api.get("/users/{userid:int}")
def get_one_user(userid:int) -> dict:
    for user in users_db:
        if user["user_id"] == userid:
            return user
    return {}

@api.get("/users/{userid:int}/name")
def get_one_user_name(userid:int) -> dict:
    for user in users_db:
        if user["user_id"] == userid:
            return {"name" : user["name"]}
    return {}

@api.get("/users/{userid:int}/subscription")
def get_one_user_subcription(userid:int) -> dict:
    for user in users_db:
        if user["user_id"] == userid:
            return {"subscription" : user["subscription"]}
    return {}

class User(BaseModel):
    user_id: int
    name: str
    subscription: str

@api.put("/users")
def put_users(user: User):
    users_db.append({"user_id": user.user_id,
                     "name": user.name,
                     "subscription": user.subscription})
    return user

@api.post("/users/{userid:int}")
def update_one_user(userid: int, user: dict) -> dict:
    user_idx = None
    for i, user in enumerate(users_db):
        if user["user_id"] == userid:
            user_idx = i
            the_user = user
    if user_idx is None:
        return {}
    
    the_user = the_user | user
    users_db[user_idx] = the_user
    return the_user

@api.delete("/users/{userid:int}")
def remove_one_user(userid: int):
    user_idx = None
    for i, user in enumerate(users_db):
        if user["user_id"] == userid:
            user_idx = i
    if user_idx is None:
        return {}
    pop = users_db.pop(user_idx)
    return {"status": "success",
            "user deleted": pop}

@api.get('/headers')
def get_headers(user_agent=Header(None)):
    return {
        'User-Agent': user_agent
    }

class Computer(BaseModel):
    """A computer object"""
    computerid: int
    cpu: str | None = None
    gpu: str | None = None
    price: float

@api.put("/computer", name="Create a new computer", tags=['home', 'items'])
def put_computer(computer: Computer):
    """Creates a new computer within the database
    """
    return computer

@api.get("/cutom", name="Get custom Header")
def get_content(custom_deader: str = Header(None, description='My own personal header')):
    return {
        "Custom-header" : custom_deader
    }
