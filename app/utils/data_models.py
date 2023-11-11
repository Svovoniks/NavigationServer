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
    key: str
    trail: List[Any]

class UserJSON(BaseModel):
    authenticated: bool = True
    name: str = ''
    email: str = ''
    session_key: str = ''

