from typing import Any, Dict
from app.utils import routing
from app.utils.DataBase import User_DataBase
from app.utils.data_models import LoginJSON, RegisterJSON, SessionJSON, UserJSON
from app.utils.data_models import TrailJSON
from fastapi import FastAPI

from app.utils.user import User

app = FastAPI()

@app.get("/get-route/{startLat}/{startLon}/{destLat}/{destLon}")
async def get_route(start_lat: float,
                    start_lon: float, 
                    dest_lat: float, 
                    dest_lon: float) -> Dict[Any, Any]:
    start = (start_lat, start_lon)
    dest = (dest_lat, dest_lon)

    route = routing.get_route(start, dest)

    return {'route': route}


@app.post("/get-trails/")
async def get_trails(key_json: SessionJSON):
    # TODO
    pass


@app.post("/add-trail/")
async def add_trail(key_json: TrailJSON):
    # TODO
    pass


@app.post("/get-user/")
async def get_user(key_json: SessionJSON) -> UserJSON:
    return User_DataBase().get_user_by_session(key_json.session_key).userJSON()


@app.post("/login/")
async def login(login_json: LoginJSON):
    return User.authenticate(login_json)


@app.post("/register/")
async def register(register_json: RegisterJSON):
    return User.register(register_json)

