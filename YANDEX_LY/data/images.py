import sqlalchemy
from .db_session import SqlAlchemyBase


class Image(SqlAlchemyBase):
    __tablename__ = "images"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    Ifile = sqlalchemy.Column(sqlalchemy.BLOB)
    Iexpansion = sqlalchemy.Column(sqlalchemy.String(255))