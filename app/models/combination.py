"""SQLAlchemy model for Combination."""
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Combination(Base):
    """SQLAlchemy model for a Combination."""
    __tablename__ = "combinations"

    id = Column(String, primary_key=True, nullable=False)
    size = Column(Integer, nullable=False)
    occurred = Column(Boolean, default=False, nullable=False)
    occurred_at = Column(DateTime, nullable=True)

    friends = relationship("Friend", secondary='friend_combinations', back_populates="combinations")
