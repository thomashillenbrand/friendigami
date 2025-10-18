from app.db.base import Base
from sqlalchemy import Column, Integer, String


class Friend(Base):
    __tablename__ = "friends"

    symbol = Column(String, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
