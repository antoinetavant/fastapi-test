from fastapi import FastAPI

api = FastAPI(title = "My API", description = "My API description", version = "1.0.0")

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

@api.get("/")
def greatings():
    return "Bienvenu à mon API"


@api.get("/users")
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
