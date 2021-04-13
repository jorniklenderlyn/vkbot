import sqlalchemy
from .db_session import SqlAlchemyBase


class TLuser(SqlAlchemyBase):
    __tablename__ = "TLusers"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    Utl_id = sqlalchemy.Column(sqlalchemy.String)
    Uclass = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Uclass_profile = sqlalchemy.Column(sqlalchemy.String, nullable=True)