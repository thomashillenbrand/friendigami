"""Service layer for Friend model operations."""
from sqlalchemy.orm import Session

from app.repositories.friend_repository import FriendRepository
from app.schemas.friend_schema import FriendBase
from app.services.combination_service import CombinationService


class FriendService:
    """Service layer for Friend model operations."""

    def __init__(self, db: Session):
        self.friend_repo = FriendRepository(db)
        self.combo_service = CombinationService(db)

    def get_friend(self, symbol: str) -> FriendBase | None:
        """Retrieve a Friend by symbol."""
        return self.friend_repo.get_by_symbol(symbol=symbol)

    def create_friend(self, symbol: str, first_name: str, last_name: str) -> FriendBase:
        """Add a new Friend and generate new combinations."""
        if self.friend_repo.get_by_symbol(symbol) is not None:
            raise ValueError(f"Friend with symbol '{symbol}' already exists.")
        friend = self.friend_repo.create(symbol=symbol, first_name=first_name, last_name=last_name)
        self.combo_service.generate_for_new_friend(symbol)
        return friend

    def remove_friend(self, symbol: str) -> bool:
        """Remove a Friend and all related combinations."""
        if self.friend_repo.get_by_symbol(symbol) is None:
            raise ValueError(f"Friend with symbol '{symbol}' does not exist.")
        self.combo_service.remove_for_friend(symbol)
        return self.friend_repo.delete(symbol=symbol)

    def modify_friend(self, symbol: str, new_symbol: str | None = None,
                      first_name: str | None = None, last_name: str | None = None) -> FriendBase | None:
        """Modify an existing Friend's details."""
        friend = self.friend_repo.get_by_symbol(symbol)
        if friend is None:
            raise ValueError(f"Friend with symbol '{symbol}' does not exist.")

        updated = self.friend_repo.update(
            symbol=symbol, new_symbol=new_symbol,
            first_name=first_name, last_name=last_name,
        )

        # If symbol changed, regenerate all combinations
        if new_symbol and new_symbol != symbol:
            self.combo_service.regenerate_all()

        return updated
