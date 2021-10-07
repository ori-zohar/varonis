import json
from sanic import Sanic
from sanic.response import json as sanic_json
from sanic_jwt import exceptions, protected
from sanic_jwt import initialize
from typing import List, Dict

class User:
    def __init__(self, uid, username, password):
        self.user_id = uid
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}

users = []
with open("config.json") as f:
    config = json.load(f)
    users.append(User(1, config["username"], config["password"]))

username_table = {u.username: i for i in users}
userid_table = {u.user_id: j for j in users}

async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user

def normalize_value(value: Dict[str, str]) -> str:
    return [val
            for key, val in value.items()
            if "val" in key.lower()][0]

def normalize_list(values: List[Dict[str, str]]) -> Dict[str, str]:
    return {value["name"]: normalize_value(value) for
            value in values}


app = Sanic(name="welcome to web site varonis")
initialize(app, authenticate=authenticate)

@app.post('/normalize')
@protected()
async def post_handler(request):
    return sanic_json(normalize_list(request.json))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=1234)