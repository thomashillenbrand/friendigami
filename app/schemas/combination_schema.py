"""Pydantic schemas for Combination."""
from datetime import datetime

from pydantic import BaseModel


class CombinationBase(BaseModel):
    """Schema for Combination."""
    id: str
    size: int
    occurred: bool = False
    occurred_at: datetime | None = None
    friends: list[str]  # List of friend symbols
