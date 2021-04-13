import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase


class Job(SqlAlchemyBase):
    __tablename__ = 'events'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           autoincrement=True, primary_key=True)
    date_of_publiction = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    Etitle_of_event = sqlalchemy.Column(sqlalchemy.String)
    Edate_of_start_event = sqlalchemy.Column(sqlalchemy.Date)
    Edate_of_finish_event = sqlalchemy.Column(sqlalchemy.Date)
    Estatus_of_speciality = sqlalchemy.Column(sqlalchemy.String, default='all')
    Estatus_of_school = sqlalchemy.Column(sqlalchemy.String, default='all')
    Estatus_of_class = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default='all')
    Ephoto = sqlalchemy.Column(sqlalchemy.Integer)
    Edescription = sqlalchemy.Column(sqlalchemy.String, nullable=True)