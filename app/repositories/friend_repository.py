"""Friend Repository"""
from app.models.friend import Friend
from app.db.session import SessionLocal

class FriendRepository:
    """Repository for Friend model CRUD operations."""
    def __init__(self):
        pass

    # TODO:
    #  - implement methods using schemas
    #  - add logging instead of print statements
    #  - handle specific exceptions

    def create(self, name: str, symbol: str) -> Friend:
        """Create a new Friend record in the database."""
        friend = Friend(name=name, symbol=symbol)
        with SessionLocal() as db:
            try:
                db.add(friend)
                db.commit()
                db.refresh(friend)
            except Exception as e:
                db.rollback()
                print(f"Error occurred: {e}")
            finally:
                db.close()

        return friend

    def delete(self, symbol) -> bool:
        """Delete a Friend record from the database by symbol."""
        result = True
        with SessionLocal() as db:
            try:
                friend = db.query(Friend).filter(Friend.symbol == symbol).first()
                if friend:
                    db.delete(friend)
                    db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error occurred: {e}")
                result =  False
            finally:
                db.close()
        return result


    def update(self, friend_id, name=None, symbol=None) -> Friend:
        """Update a Friend record in the database."""
        with SessionLocal() as db:
            try:
                friend = db.query(Friend).filter(Friend.id == friend_id).first()
                if friend:
                    friend.name = name if name is not None else friend.name
                    friend.symbol = symbol if symbol is not None else friend.symbol
                    db.commit()
                    db.refresh(friend)
            except Exception as e:
                db.rollback()
                print(f"Error occurred: {e}")
            finally:
                db.close()


    def get_all(self) -> list[Friend]:
        """"Retrieve all Friend records from the database."""
        with SessionLocal() as db:
            friends = db.query(Friend).all()
            return friends


    def get_by_symbol(self, symbol) -> Friend:
        """Retrieve a Friend record from the database by symbol."""
        with SessionLocal() as db:
            friend = db.query(Friend).filter(Friend.symbol == symbol).first()
            return friend


    def get_by_id(self, friend_id) -> Friend:
        """Retrieve a Friend record from the database by ID."""
        with SessionLocal() as db:
            friend = db.query(Friend).filter(Friend.id == friend_id).first()
            return friend