import sqlalchemy
from .db_session import SqlAlchemyBase


class VKuser(SqlAlchemyBase):
    __tablename__ = "Vkusers"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    Uvk_id = sqlalchemy.Column(sqlalchemy.String)
    Uclass = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Uclass_profile = sqlalchemy.Column(sqlalchemy.String, nullable=True)