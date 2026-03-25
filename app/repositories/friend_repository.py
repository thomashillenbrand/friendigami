"""Friend Repository"""
from sqlalchemy.orm import Session

from app.models.friend import Friend
from app.schemas.friend_schema import FriendBase


class FriendRepository:
    """Repository for Friend model CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, symbol: str, first_name: str, last_name: str) -> FriendBase:
        """Create a new Friend record."""
        friend = Friend(symbol=symbol, first_name=first_name, last_name=last_name)
        self.db.add(friend)
        self.db.commit()
        self.db.refresh(friend)
        return self._to_schema(friend)

    def delete(self, symbol: str) -> bool:
        """Delete a Friend record by symbol."""
        friend = self.db.query(Friend).filter(Friend.symbol == symbol).first()
        if not friend:
            return False
        self.db.delete(friend)
        self.db.commit()
        return True

    def update(self, symbol: str, new_symbol: str | None = None,
               first_name: str | None = None, last_name: str | None = None) -> FriendBase | None:
        """Update a Friend record."""
        friend = self.db.query(Friend).filter(Friend.symbol == symbol).first()
        if not friend:
            return None
        if new_symbol is not None:
            friend.symbol = new_symbol
        if first_name is not None:
            friend.first_name = first_name
        if last_name is not None:
            friend.last_name = last_name
        self.db.commit()
        self.db.refresh(friend)
        return self._to_schema(friend)

    def get_all(self) -> list[FriendBase]:
        """Retrieve all Friend records."""
        friends = self.db.query(Friend).all()
        return [self._to_schema(f) for f in friends]

    def get_by_symbol(self, symbol: str) -> FriendBase | None:
        """Retrieve a Friend by symbol."""
        friend = self.db.query(Friend).filter(Friend.symbol == symbol).first()
        return self._to_schema(friend) if friend else None

    def get_all_symbols(self) -> list[str]:
        """Retrieve all friend symbols."""
        return [f.symbol for f in self.db.query(Friend.symbol).all()]

    @staticmethod
    def _to_schema(friend: Friend) -> FriendBase:
        return FriendBase(
            symbol=friend.symbol,
            first_name=friend.first_name,
            last_name=friend.last_name,
        )
