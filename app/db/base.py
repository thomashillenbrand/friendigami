from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# SQLite file DB in project root
SQLALCHEMY_DATABASE_URL = "sqlite:///friendigami.db"

# For SQLite and some multi-threaded setups
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()
