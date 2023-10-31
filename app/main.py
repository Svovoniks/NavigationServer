from app.utils import routing
from app.utils.user import user_from_key, LoginJSON, RegisterJSON, KeyJSON, TrailJSON
from fastapi import FastAPI

app = FastAPI()


@app.get("/get-route/{startLat}/{startLon}/{destLat}/{destLon}")
async def get_route(start_lat: float, start_lon: float, dest_lat: float, dest_lon: float):
    start = (start_lat, start_lon)
    dest = (dest_lat, dest_lon)

    route = routing.get_route_a_star(start, dest)

    return {'route': route}


@app.post("/get-trails/")
async def get_trails(key_json: KeyJSON):
    # TODO
    pass


@app.post("/add-trail/")
async def add_trail(key_json: TrailJSON):
    # TODO
    pass


@app.post("/get-user/")
async def get_user(key_json: KeyJSON):
    return user_from_key(key_json.key)


@app.post("/login/")
async def login(login_json: LoginJSON):
    # TODO
    pass


@app.post("/register/")
async def register(register_json: RegisterJSON):
    # TODO
    pass
