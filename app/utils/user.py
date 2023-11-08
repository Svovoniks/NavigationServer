from hashlib import sha256
from typing import Any, List
from pydantic import BaseModel

from app.utils.trail import Trail
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
    name: str
    email: str
    
    
class User:
    name: str
    email: str
    password_hash: str
    trails: List[Trail]
    session_key: str
    
    def __init__(self, name: str, email: str, password_hash: str, session_key: str) -> None:
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.session_key = session_key

    def authenticate(self, password: str) -> bool:
        return self.password_hash == sha256(password.encode('ascii')).hexdigest()

    def add_user(self) -> None:
        # TODO
        pass

    def userJSON(self) -> UserJSON:
        return UserJSON(name=self.name, email=self.email)
