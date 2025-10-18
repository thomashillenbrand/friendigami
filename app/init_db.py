
"""Initialize the database by creating tables if they do not exist."""
from app.db.base import Base, engine
from app.models import friend

from app.repositories.friend_repository import FriendRepository

# TODO: use alembic for migrations

def create_tables():
    """Create database tables defined by SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()

    friend_repo = FriendRepository()

    friend_repo.update(friend_id=1, name="Thomas", symbol="T")
    friend_repo.create(name="Marin Williams", symbol="M")

    print("Database tables created (or already existed): friendigami.db")
