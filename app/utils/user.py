import secrets
from hashlib import sha256
from typing import List
import app.utils.DataBase as DB
from app.utils.data_models import LoginJSON, RegisterJSON, SessionJSON, UserJSON

from app.utils.trail import Trail
class User:
    user_id: int | None
    name: str
    email: str
    password_hash: str
    trails: List[Trail]
    session_key: str | None
    
    def __init__(self, 
                user_id: int | None,
                name: str,
                email: str,
                password_hash: str,
                session_key: str | None) -> None:
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.session_key = session_key

    def add_user(self) -> None:
        self.user_id = DB.User_DataBase().add_user(self)


    def register_new_session(self) -> SessionJSON:
        key = User.generate_session_key()
        self.session_key = key
        DB.User_DataBase().add_session_key(self)
        return SessionJSON(session_key=key)

    def userJSON(self) -> UserJSON:
        return UserJSON(name=self.name, 
                        email=self.email, 
                        session_key=self.session_key) # type: ignore
    
    @staticmethod
    def generate_session_key():
        return secrets.token_urlsafe(30)

    @staticmethod
    def get_password_hash(password: str):
        return sha256(password.encode('ascii')).hexdigest()
    
    @staticmethod
    def user_from_registerJSON(register: RegisterJSON) -> 'User':
        return User(None, 
                    register.username, 
                    register.email,
                    User.get_password_hash(register.password),
                    None)

    @staticmethod
    def authenticate(login: LoginJSON) -> UserJSON:
        user = DB.User_DataBase().get_user_by_name(login.username)
        if not user.password_hash == User.get_password_hash(login.password):
            return UserJSON(authenticated=False)
        
        user.register_new_session()
        return user.userJSON()
    
    @staticmethod
    def register(register: RegisterJSON) -> UserJSON:
        user = User.user_from_registerJSON(register)
        if not DB.User_DataBase().username_available(user):
            return UserJSON(authenticated=False)
        
        user.add_user()
        user.register_new_session()
        return user.userJSON()
    


