from pydantic import BaseModel
from typing import Any, List

class LoginJSON(BaseModel):
    username: str
    password: str

class RegisterJSON(BaseModel):
    username: str
    password: str
    email: str

class SessionJSON(BaseModel):
    session_key: str

class TrailJSON(BaseModel):
    authenticated: bool = True
    session_key: str = ''
    trails: List[dict[str, Any]] = [] # list of {'id': id, 'name': name, points: [{'x': x, 'y': y}]}
    
class TrailIDJSON(BaseModel):
    session_key: str = ''
    trail_id: int

class UserJSON(BaseModel):
    authenticated: bool = True
    name: str = ''
    email: str = ''
    session_key: str = ''

