import os
from typing import Any, List
from sqlalchemy import CursorResult, Engine, Executable, Identity, MetaData, create_engine
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy import insert, delete, select
from app.utils.trail import Trail
from app.utils.user import User
from sqlalchemy.orm.exc import NoResultFound

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
    Column("x", DOUBLE_PRECISION),
    Column("y", DOUBLE_PRECISION),
    Column("point_index", Integer),
)
trail_user_table = Table(
    "user_trail",
    trail_metadata,
    Column("trail_id", Integer, primary_key=True),
    Column("user_id", Integer),
)


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

    def execute(self, stmnt: Executable) -> CursorResult[Any]:
        with self.engine.connect() as conn:
            result = conn.execute(stmnt)
            conn.commit()

            return result


class Trail_DataBase(DataBase):
    def __init__(self) -> None:
        super(Trail_DataBase, self).__init__()

    def add_trail(self, trail: Trail) -> None:
        statement = insert(trail_table).values(x=trail.x,
                                               y=trail.y,
                                               point_index=trail.point_index)
        print(self.execute(statement).first())

    def remove_trail(self, trail: Trail) -> None:
        statement = delete(trail_table).where(trail_table.c.id == trail.id)  # type: ignore
        self.execute(statement)
        statement = delete(trail_user_table).where(trail_user_table.c.trail_id == trail.id)  # type: ignore
        self.execute(statement)

    def get_trail_by_id(self, trail_id: int) -> Trail:
        statement = select(trail_table.c.id,
                           trail_table.c.x,
                           trail_table.c.y,
                           trail_table.c.point_index, ).where(trail_table.c.id == trail_id)
        result = self.execute(statement).all()
        try:
            print(result)
            return Trail(result[0].id, result[0].x, result[0].y, result[0].point_index)
        except NoResultFound:
            raise ValueError(f"Trail with ID {trail_id} not found.")

    def get_user_trails(self, user: User) -> List[Trail]:
        statement = select(trail_table.c.id,
                           trail_table.c.x,
                           trail_table.c.y,
                           trail_table.c.point_index, ).where(trail_user_table.c.trail_id == trail_table.c.id) \
            .where(trail_user_table.c.user_id == user.id)
        result = self.execute(statement).all()
        trails = [
            Trail(trail_id=row.id, x=row.x, y=row.y, point_index=row.point_index)
            for row in result]
        return trails


class User_DataBase(DataBase):
    def __init__(self) -> None:
        super(User_DataBase, self).__init__()

    def add_user(self, user: User) -> None:
        statement = insert(user_table).values(email=user.email,
                                              username=user.name,
                                              password_hash=user.password_hash)
        print(self.execute(statement).first())

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

    def add_session_key(self, user: User) -> None:
        statement = insert(session_table).values(user_id=user.user_id,
                                                 session_key=user.session_key)
        self.execute(statement)

    def remove_session_key(self, user: User) -> None:
        statement = delete(session_table).where(session_table.c.user_id == user.id)  # type: ignore
        self.execute(statement)

    def validate_session_key(self, session_key: str) -> bool:
        statement = select(session_table).where(session_table.c.session_key == session_key)
        result = self.execute(statement)
        return len(result.all()) != 0

    '''
    use with valid session key
    '''

    def get_user_by_session(self, session_key: str) -> User:
        statement = select(user_table.c.id,
                           user_table.c.email,
                           user_table.c.username,
                           user_table.c.password_hash, )  # .where(session_table.c.session_key == session_key).where(session_table.c.user_id == user_table.c.id)
        result = self.execute(statement).all()
        print(result)

        # return User(result[0], result[1], result[2], result[3]) # type: ignore


def test():
    user = User("lol", "lol.com", "some_hash", User.generate_session_key())
    db = User_DataBase()
    db.add_user(user)
    # db.add_session_key(user)
    print(db.get_user_by_session(User.generate_session_key()))
    print(db.validate_session_key(User.generate_session_key()))
