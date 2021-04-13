import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


class LessonsList(SqlAlchemyBase):
    __tablename__ = "lessonslists"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    LdictImages = sqlalchemy.Column(sqlalchemy.String)
    Ldate = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now())