"""Friend Repository"""
from app.models.friend import Friend
from app.db.session import SessionLocal
from app.schemas.friend_schema import FriendBase

class FriendRepository:
    """Repository for Friend model CRUD operations."""

    # TODO:
    #  - implement methods using schemas
    #  - add logging instead of print statements
    #  - handle specific exceptions
    #  - add new methods as needed
    #

    def create(self, symbol: str, first_name: str, last_name: str) -> FriendBase | None:
        """Create a new Friend record in the database."""
        friend = Friend(symbol=symbol, first_name=first_name, last_name=last_name)
        with SessionLocal() as db:
            try:
                db.add(friend)
                db.commit()
                db.refresh(friend)
            except Exception as e: # pylint: disable=broad-except
                db.rollback()
                print(f"Error occurred: {e}")
                friend = None
            finally:
                db.close()

        return FriendBase(
            symbol=friend.symbol,
            first_name=friend.first_name,
            last_name=friend.last_name
        ) if friend else None


    def delete(self, symbol: str) -> bool:
        """Delete a Friend record from the database by symbol."""
        result = True
        with SessionLocal() as db:
            try:
                friend = db.query(Friend).filter(Friend.symbol == symbol).first()
                if friend:
                    db.delete(friend)
                    db.commit()
            except Exception as e: # pylint: disable=broad-except
                db.rollback()
                print(f"Error occurred: {e}")
                result =  False
            finally:
                db.close()
        return result


    def update(self, symbol: str, new_symbol: str=None,
               first_name: str=None, last_name: str=None) -> FriendBase | None:
        """Update a Friend record in the database."""
        with SessionLocal() as db:
            try:
                friend = db.query(Friend).filter(Friend.symbol == symbol).first()
                if friend:
                    friend.symbol = new_symbol if new_symbol is not None else friend.symbol
                    friend.first_name = first_name if first_name is not None else friend.first_name
                    friend.last_name = last_name if last_name is not None else friend.last_name
                    db.commit()
                    db.refresh(friend)
            except Exception as e: # pylint: disable=broad-except
                db.rollback()
                print(f"Error occurred: {e}")
                friend = None
            finally:
                db.close()

        return FriendBase(
            symbol=friend.symbol,
            first_name=friend.first_name,
            last_name=friend.last_name
        ) if friend else None


    def get_all(self) -> list[FriendBase]:
        """"Retrieve all Friend records from the database."""
        with SessionLocal() as db:
            friends = db.query(Friend).all()
            return [
                FriendBase(
                    symbol=friend.symbol, 
                    first_name=friend.first_name,
                    last_name=friend.last_name
                ) for friend in friends
            ]


    def get_by_symbol(self, symbol: str) -> FriendBase | None:
        """Retrieve a Friend record from the database by symbol."""
        with SessionLocal() as db:
            friend = db.query(Friend).filter(Friend.symbol == symbol).first()
            return FriendBase(
                symbol=friend.symbol,
                first_name=friend.first_name,
                last_name=friend.last_name
            ) if friend else None
