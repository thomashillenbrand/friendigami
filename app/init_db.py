
"""Initialize the database by creating tables if they do not exist."""
from app.db.base import Base, engine
from app.models import friend # pylint: disable=unused-import

from app.services.friend_service import FriendService

# TODO: use alembic for migrations

def create_tables():
    """Create database tables defined by SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()

    friend_service = FriendService()

    friend_service.add_friend(symbol="T", first_name="Tom", last_name="Hillenbrand")
    friend_service.add_friend(symbol="M", first_name="Marin", last_name="Williams")

    print("Database tables created (or already existed): friendigami.db")
