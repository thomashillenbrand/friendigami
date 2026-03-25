"""Import all models so SQLAlchemy registers them."""
from app.models.friend import Friend  # noqa: F401
from app.models.combination import Combination  # noqa: F401
from app.models.friend_combinations import friend_combinations  # noqa: F401
