"""Define the Friend model for the database."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Friend(Base):
    """SQLAlchemy model for a Friend."""
    __tablename__ = "friends"

    symbol = Column(String, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    combinations = relationship("Combination", secondary='friend_combinations', back_populates="friends")
