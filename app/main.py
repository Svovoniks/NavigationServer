from app.utils import routing
from app.utils.DataBase import User_DataBase
from app.utils.user import LoginJSON, RegisterJSON, SessionJSON, TrailJSON
from fastapi import FastAPI

app = FastAPI()


@app.get("/get-route/{startLat}/{startLon}/{destLat}/{destLon}")
async def get_route(start_lat: float, start_lon: float, dest_lat: float, dest_lon: float):
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
async def get_user(key_json: SessionJSON):
    return User_DataBase().get_user_by_session(key_json.session_key)


@app.post("/login/")
async def login(login_json: LoginJSON):
    # TODO
    pass


@app.post("/register/")
async def register(register_json: RegisterJSON):
    # TODO
    pass

