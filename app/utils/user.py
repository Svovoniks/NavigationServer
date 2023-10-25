from hashlib import sha256
from pydantic import BaseModel


class User:
    def __init__(self, name, email, password_hash, trails, key):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.trails = trails
        self.key = key

    def authenticate(self, password):
        return self.password_hash == sha256(password).hexdigest()

    def add_user(self):
        # TODO
        pass

    def get_user(self):
        return {
            'name': self.name,
            'email': self.email,
            'trails': self.trails
        }


class LoginJSON(BaseModel):
    username: str
    password: str


class RegisterJSON(BaseModel):
    username: str
    password: str
    email: str


class KeyJSON(BaseModel):
    key: str


class TrailJSON(BaseModel):
    key: str
    trail: list


def user_from_key(key):
    # TODO
    pass
