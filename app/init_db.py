"""Initialize the database by creating tables if they do not exist."""
from app.db.base import Base, engine
from app.db.session import SessionLocal
from app.models import friend, combination, friend_combinations  # noqa: F401
from app.services.combination_service import CombinationService
from app.repositories.friend_repository import FriendRepository


def create_tables():
    """Create database tables defined by SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


def seed_and_generate():
    """Optionally seed friends and regenerate all combinations."""
    with SessionLocal() as db:
        repo = FriendRepository(db)
        if repo.get_all():
            print("Friends already exist, skipping seed.")
        else:
            print("Seeding friends...")
            repo.create(symbol="TH", first_name="Tom", last_name="H")
            repo.create(symbol="MW", first_name="Marin", last_name="W")

        service = CombinationService(db)
        count = service.regenerate_all()
        print(f"Generated {count} combinations.")


if __name__ == "__main__":
    create_tables()
    seed_and_generate()
    print("Database initialized: friendigami.db")
