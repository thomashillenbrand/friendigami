"""Define the Friend model for the database."""
from sqlalchemy import Column, String

from app.db.base import Base


class Friend(Base):
    """SQLAlchemy model for a Friend."""
    __tablename__ = "friends"

    symbol = Column(String, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
