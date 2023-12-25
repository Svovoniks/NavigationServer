import os
from typing import Any, List
from sqlalchemy import CursorResult, Engine, Executable, MetaData, create_engine
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy import insert, delete, select
from app.utils.data_models import TrailIDJSON
from app.utils.trail import Trail
from app.utils.user import User

user_metadata = MetaData(schema='user')
trail_metadata = MetaData(schema='trail')

user_table = Table(
    "user_data",
    user_metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("username", String),
    Column("password_hash", String),
)
session_table = Table(
    "user_session",
    user_metadata,
    Column("user_id", Integer, primary_key=True),
    Column("session_key", String),
)
trail_table = Table(
    "trail_point",
    trail_metadata,
    Column("id", Integer, primary_key=True), 
    Column("x", DOUBLE_PRECISION), # type: ignore
    Column("y", DOUBLE_PRECISION), # type: ignore
    Column("point_index", Integer),
)
trail_user_table = Table(
    "user_trail",
    trail_metadata,
    Column("trail_id", Integer, primary_key=True),
    Column("trail_name", String),
    Column("user_id", Integer),
)


class DataBase:
    engine: Engine

    def __init__(self) -> None:
        self.engine = self.connect()

    def connect(self) -> Engine:
        db_name = os.environ['DB_NAME']
        db_host = os.environ['POSTGRES_HOST']
        db_port = os.environ['POSTGRES_PORT']
        db_user = os.environ['POSTGRES_USER']
        db_password = os.environ['POSTGRES_PASSWORD']
        return create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    def execute(self, stmnt: Executable) -> CursorResult[Any]:
        with self.engine.connect() as conn:
            result = conn.execute(stmnt)
            conn.commit()

            return result


class Trail_DataBase(DataBase):
    def __init__(self) -> None:
        super(Trail_DataBase, self).__init__()

    def add_trail(self, trail: Trail) -> None:
        statement = insert(trail_user_table).values(
            trail_name = trail.trail_name,
            user_id = trail.user_id,
        )
        trail.trail_id = self.execute(statement).inserted_primary_key[0] # type: ignore
        
        trail_insert_list = []
        for idx, i in enumerate(trail.points):
            trail_insert_list.append({       # type: ignore
                'id': trail.trail_id,  
                'x': i['x'],
                'y': i['y'],
                'point_index': idx
            })
        
        statement = insert(trail_table).values(trail_insert_list)
        self.execute(statement)
        
        
    def remove_trail_by_id(self, trail_id: int) -> None:
        statement = delete(trail_table).where(trail_table.c.id == trail_id)  # type: ignore
        self.execute(statement)
        statement = delete(trail_user_table).where(trail_user_table.c.trail_id == trail_id)  # type: ignore
        self.execute(statement)

    def remove_trail(self, trail: Trail) -> None:
        self.remove_trail_by_id(trail.trail_id)
        
    def verify_trail_owner(self, trail_id_json: TrailIDJSON) -> bool:
        user = User_DataBase().get_user_by_session(trail_id_json.session_key)
        statement = select(
            trail_user_table.c.user_id,
        ).where(trail_user_table.c.trail_id == trail_id_json.trail_id).where(trail_user_table.c.user_id == user.user_id)
        
        return len(self.execute(statement).all()) != 0
        
    def get_trail_points_by_trail_id(self, trail_id: int) -> List[dict[str, float]]:
        statement = select(
            trail_table.c.x,
            trail_table.c.y,
            trail_table.c.point_index, 
        ).where(trail_table.c.id == trail_id)
        
        points = []
        
        for i in sorted(self.execute(statement).all(), key=lambda a: a[2]):
            points.append({'x': i[0], 'y': i[1]}) # type: ignore
        
        return points # type: ignore
        

    def get_user_trails(self, user: User) -> List[Trail]:
        statement = select(
            trail_user_table.c.trail_id,
            trail_user_table.c.trail_name,
            trail_user_table.c.user_id,
        ).where(trail_user_table.c.user_id == user.user_id)
        
        trails = []
        
        for i in self.execute(statement).all():
            trail = Trail(
                i[0],
                user.user_id,      # type: ignore
                i[1],
                self.get_trail_points_by_trail_id(i[0])
            )
            trails.append(trail)   # type: ignore
        
        return trails              # type: ignore


class User_DataBase(DataBase):
    def __init__(self) -> None:
        super(User_DataBase, self).__init__()
    
    def username_available(self, username: str) -> bool:
        statement = select(user_table).where(user_table.c.username == username)
        r = self.execute(statement).all()
        return len(r) == 0
        
    '''
    use with unique usernames only 
    '''        
    def add_user(self, user: User) -> int:
        statement = insert(user_table).values(email=user.email, 
                                  username=user.name, 
                                  password_hash=user.password_hash)
        self.execute(statement)

        return self.get_user_by_name(user.name).user_id # type: ignore

    
    def remove_user(self, user: User) -> None:
        statement = delete(user_table).where(user_table.c.id == user.id)  # type: ignore
        self.execute(statement)
        statement = delete(session_table).where(session_table.c.user_id == user.id)  # type: ignore
        self.execute(statement)
        statement = delete(trail_table).where(trail_user_table.c.trail_id == trail_table.c.id) \
            .where(trail_user_table.c.user_id == user.id)  # type: ignore
        self.execute(statement)
        statement = delete(trail_user_table).where(trail_user_table.c.user_id == user.id)  # type: ignore
        self.execute(statement)
        
    def session_key_available(self, key: str) -> bool:
        statement = select(session_table).where(session_table.c.session_key == key)
        r = self.execute(statement).all()
        return len(r) == 0
    
    '''
    use with unique session keys only 
    '''       
    def add_session_key(self, user: User) -> None:
        statement = insert(session_table).values(user_id=user.user_id,
                                                 session_key=user.session_key)
        self.execute(statement)
    
    def remove_session_key(self, key: str) -> None:
        statement = delete(session_table).where(session_table.c.session_key == key) # type: ignore
        self.execute(statement)
    
    '''
    use with valid session keys only
    '''
    def get_user_by_session(self, session_key: str) -> User:
        statement = select(
            user_table.c.id,
            user_table.c.email,
            user_table.c.username,
            user_table.c.password_hash).where(session_table.c.session_key == session_key).where(session_table.c.user_id == user_table.c.id
        )
        r = self.execute(statement).first()

        return User(r[0], r[1], r[2], r[3], session_key) # type: ignore
    
    '''
    use with valid usernames only
    '''
    def get_user_by_name(self, username: str):
        statement = select(user_table.c.id,
                           user_table.c.username,
                           user_table.c.email,
                           user_table.c.password_hash).where(user_table.c.username == username)
        r = self.execute(statement).first()
        return User(r[0], r[1], r[2], r[3], None) # type: ignore
