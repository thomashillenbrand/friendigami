"""Service layer for Friend model operations."""
from app.models.friend import Friend
from app.repositories.friend_repository import FriendRepository

class FriendService:
    """Service layer for Friend model operations."""

    # fixme TODO:
    #  - implement methods using schemas
    #  - add new methods as needed
    #

    def __init__(self):
        self.friend_repo = FriendRepository()

    def get_friend(self, symbol: str) -> Friend:
        """Retrieve a Friend by symbol."""
        return self.friend_repo.get_by_symbol(symbol=symbol)

    def add_friend(self, symbol: str, first_name: str, last_name: str) -> Friend:
        """Add a new Friend."""
        if self.friend_repo.get_by_symbol(symbol) is not None:
            raise ValueError(f"Friend with symbol '{symbol}' already exists.")
        return self.friend_repo.create(symbol=symbol, first_name=first_name, last_name=last_name)

    def remove_friend(self, symbol: str) -> bool:
        """Remove a Friend by symbol."""
        if (self.friend_repo.get_by_symbol(symbol)) is None:
            raise ValueError(f"Friend with symbol '{symbol}' does not exist.")
        friend = self.friend_repo.get_by_symbol(symbol)
        return self.friend_repo.delete(symbol=friend.symbol)

    def modify_friend(self, symbol: str, new_symbol: str = None, first_name: str = None, last_name: str = None) -> Friend:
        """Modify an existing Friend's details."""
        friend = self.friend_repo.get_by_symbol(symbol)
        if friend is None:
            raise ValueError(f"Friend with symbol '{symbol}' does not exist.")
        return self.friend_repo.update(symbol=symbol, new_symbol=new_symbol, first_name=first_name, last_name=last_name)
    