import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Admin(SqlAlchemyBase):
    __tablename__ = 'admins'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    Astatus = sqlalchemy.Column(sqlalchemy.Integer)
    AName = sqlalchemy.Column(sqlalchemy.String)
    Alogin = sqlalchemy.Column(sqlalchemy.String)
    Apassword = sqlalchemy.Column(sqlalchemy.String)