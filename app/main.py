from typing import Any, Dict
from app.utils import routing
from app.utils.DataBase import User_DataBase # DO NOT TOUCH (prevents circular import)     # type: ignore
from app.utils.DataBase import Trail_DataBase # DO NOT TOUCH (prevents circular import)     # type: ignore
from app.utils.data_models import LoginJSON, RegisterJSON, SessionJSON, UserJSON
from app.utils.data_models import TrailJSON
from fastapi import FastAPI

from app.utils.user import User
from app.utils.trail import Trail

app = FastAPI()

@app.get("/get-route/")
async def get_route(start_lat: float,
                    start_lon: float, 
                    dest_lat: float, 
                    dest_lon: float) -> Dict[Any, Any]:
    start = (start_lat, start_lon)
    dest = (dest_lat, dest_lon)
    
    route = routing.get_route(start, dest)
    
    return {'route': route}
    

@app.post("/get-trails/")
async def get_trails(session: SessionJSON) -> TrailJSON:
    return Trail.get_user_trails(session)


@app.post("/add-trail/")
async def add_trail(trail_json: TrailJSON) -> TrailJSON:
    return Trail.add_trail(trail_json)


@app.post("/get-user/")
async def get_user(session_json: SessionJSON) -> UserJSON:
    return User.login(session_json)


@app.post("/login/")
async def login(login_json: LoginJSON) -> UserJSON:
    return User.authenticate(login_json)


@app.post("/register/")
async def register(register_json: RegisterJSON) -> UserJSON:
    return User.register(register_json)

