
"""Define the association table for Friend and Combination many-to-many relationship."""
from sqlalchemy import Column, ForeignKey, String, Table

from app.db.base import Base

friend_combinations = Table('friend_combinations', Base.metadata,
    Column('friend_symbol', String, ForeignKey('friends.symbol'), primary_key=True),
    Column('combination_id', String, ForeignKey('combinations.id'), primary_key=True)
)
