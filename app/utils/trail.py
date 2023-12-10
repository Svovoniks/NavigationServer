from typing import List
import app.utils.DataBase as DB
from app.utils.data_models import SessionJSON, TrailIDJSON, TrailJSON

class Trail:
    trail_id: int
    user_id: int
    trail_name: str
    points: List[dict[str, float]] # list of {'x': x, 'y': y}

    def __init__(self, trail_id: int, user_id: int, trail_name: str, points: List[dict[str, float]]) -> None:
        self.trail_id = trail_id
        self.user_id = user_id
        self.trail_name = trail_name
        self.points = points
    
    @staticmethod
    def get_user_trails(session: SessionJSON) -> TrailJSON:
        user = User.get_user_by_session(session)
        if user == None:
            return TrailJSON(authenticated=False)
        
        trails = []
        for i in DB.Trail_DataBase().get_user_trails(user):
            trails.append({'id': i.trail_id, 'name': i.trail_name, 'points': i.points}) # type: ignore
        
        return TrailJSON(session_key=session.session_key, trails=trails)
    
    @staticmethod
    def add_trail(trail_json: TrailJSON) -> TrailJSON:
        user = User.get_user_by_session_key(trail_json.session_key)
        if user == None:
            return TrailJSON(authenticated=False)
        
        for i in trail_json.trails:
            DB.Trail_DataBase().add_trail(Trail(-1, user.user_id, i['name'], i['points'])) # type: ignore
        
        return TrailJSON()
    
    @staticmethod
    def remove_trail(trail_id_json: TrailIDJSON):
        if DB.Trail_DataBase().verify_trail_owner(trail_id_json):
            DB.Trail_DataBase().remove_trail_by_id(trail_id_json.trail_id)
        
from app.utils.user import User