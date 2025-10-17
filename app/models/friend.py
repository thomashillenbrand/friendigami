from app.db.base import Base
from sqlalchemy import Column, Integer, String


class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, unique=True)
