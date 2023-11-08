import os
from typing import List
from sqlalchemy import Engine, create_engine

from app.utils.trail import Trail
from app.utils.user import User

class DataBase:
    engine: Engine
    
    def __init__(self) -> None:
        print("jey")
        self.engine = self.connect()

    def connect(self) -> Engine:
        db_name = os.environ['DB_NAME']
        db_host = os.environ['POSTGRES_HOST']
        db_port = os.environ['POSTGRES_PORT']
        db_user = os.environ['POSTGRES_USER']
        db_password = os.environ['POSTGRES_PASSWORD']
        return create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

class Trail_DataBase(DataBase):
    def __init__(self) -> None:
        super(Trail_DataBase, self).__init__()
    
    def add_trail(self, trail: Trail) -> None:
        # TODo
        pass
    
    def remove_trail(self, trail: Trail) -> None:
        # TODo
        pass
    
    def get_trail_by_id(self, trail_id: int) -> Trail:
        # TODO
        return Trail()
    
    def get_user_trails(self, user: User) -> List[Trail]:
        # TODO
        return [Trail(),]
        
        

class User_DataBase(DataBase):
    def __init__(self) -> None:
        super(User_DataBase, self).__init__()
    
    def add_user(self, user: User) -> None:
        # TODo
        pass
    
    def remove_user(self, user: User) -> None:
        # TODo
        pass
    
    def get_session_key(self, user: User) -> str:
        # TODo
        return ""
        
    def add_session_key(self, user: User, key: str) -> None:
        # TODo
        pass
    
    def remove_session_ke(self, user: User, key: str) -> None:
        pass
    
    def get_user_by_session(self, session_key: str) -> User:
        # TODo
        return User_DataBase().get_user_by_session("")