
"""Initialize the database by creating tables if they do not exist."""
from app.db.base import Base, engine
from app.models import friend

def create_tables():
    """Create database tables defined by SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created (or already existed): friendigami.db")
