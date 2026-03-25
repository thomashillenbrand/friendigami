"""Service layer for Combination operations."""
from itertools import combinations

from sqlalchemy.orm import Session

from app.repositories.combination_repository import CombinationRepository
from app.repositories.friend_repository import FriendRepository
from app.schemas.combination_schema import CombinationBase


def build_combo_id(symbols: list[str]) -> str:
    """Build a deterministic combination ID from sorted symbols."""
    return "-".join(sorted(symbols))


class CombinationService:
    """Service layer for combination generation and management."""

    def __init__(self, db: Session):
        self.combo_repo = CombinationRepository(db)
        self.friend_repo = FriendRepository(db)

    def get_all(self, size: int | None = None, occurred: bool | None = None) -> list[CombinationBase]:
        """Get all combinations with optional filters."""
        return self.combo_repo.get_all(size=size, occurred=occurred)

    def get_by_id(self, combo_id: str) -> CombinationBase | None:
        """Get a single combination by ID."""
        return self.combo_repo.get_by_id(combo_id)

    def toggle_occurred(self, combo_id: str) -> CombinationBase | None:
        """Toggle occurred status."""
        return self.combo_repo.toggle_occurred(combo_id)

    def mark_occurred_by_symbols(self, symbols: list[str]) -> tuple[CombinationBase | None, bool]:
        """Mark a combination as occurred given friend symbols.

        Returns (combination, was_already_occurred) or (None, False) if not found.
        """
        combo_id = build_combo_id(symbols)
        result = self.combo_repo.mark_occurred(combo_id)
        if result is None:
            return None, False
        return result

    def generate_for_new_friend(self, new_symbol: str) -> int:
        """Generate all new combinations that include the new friend."""
        all_symbols = self.friend_repo.get_all_symbols()
        other_symbols = [s for s in all_symbols if s != new_symbol]

        new_combos = []
        # For each possible group size (2 through total friends)
        for size in range(2, len(all_symbols) + 1):
            # We need groups of (size-1) from existing friends, plus the new friend
            for group in combinations(other_symbols, size - 1):
                combo_symbols = list(group) + [new_symbol]
                combo_id = build_combo_id(combo_symbols)
                new_combos.append({
                    "id": combo_id,
                    "size": size,
                    "friends": combo_symbols,
                })

        return self.combo_repo.bulk_create(new_combos)

    def remove_for_friend(self, symbol: str) -> int:
        """Remove all combinations containing the given friend."""
        return self.combo_repo.delete_containing_friend(symbol)

    def regenerate_all(self) -> int:
        """Delete all combinations and regenerate from current friends."""
        self.combo_repo.delete_all()
        all_symbols = self.friend_repo.get_all_symbols()

        all_combos = []
        for size in range(2, len(all_symbols) + 1):
            for group in combinations(all_symbols, size):
                combo_id = build_combo_id(list(group))
                all_combos.append({
                    "id": combo_id,
                    "size": size,
                    "friends": list(group),
                })

        return self.combo_repo.bulk_create(all_combos)
