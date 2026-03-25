"""Combination Repository"""
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.combination import Combination
from app.models.friend import Friend
from app.schemas.combination_schema import CombinationBase


class CombinationRepository:
    """Repository for Combination model CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, combo_id: str, size: int, friend_symbols: list[str]) -> CombinationBase:
        """Create a new Combination with associated friends."""
        friends = self.db.query(Friend).filter(Friend.symbol.in_(friend_symbols)).all()
        combination = Combination(id=combo_id, size=size)
        combination.friends = friends
        self.db.add(combination)
        self.db.commit()
        self.db.refresh(combination)
        return self._to_schema(combination)

    def bulk_create(self, combos: list[dict]) -> int:
        """Create multiple combinations. Returns count created."""
        count = 0
        for combo in combos:
            existing = self.db.query(Combination).filter(Combination.id == combo["id"]).first()
            if existing:
                continue
            friends = self.db.query(Friend).filter(Friend.symbol.in_(combo["friends"])).all()
            combination = Combination(id=combo["id"], size=combo["size"])
            combination.friends = friends
            self.db.add(combination)
            count += 1
        self.db.commit()
        return count

    def delete(self, combo_id: str) -> bool:
        """Delete a Combination by id."""
        combination = self.db.query(Combination).filter(Combination.id == combo_id).first()
        if not combination:
            return False
        self.db.delete(combination)
        self.db.commit()
        return True

    def delete_containing_friend(self, symbol: str) -> int:
        """Delete all combinations that contain a given friend. Returns count deleted."""
        combos = (
            self.db.query(Combination)
            .filter(Combination.friends.any(Friend.symbol == symbol))
            .all()
        )
        count = len(combos)
        for c in combos:
            self.db.delete(c)
        self.db.commit()
        return count

    def get_by_id(self, combo_id: str) -> CombinationBase | None:
        """Retrieve a Combination by id."""
        combo = self.db.query(Combination).filter(Combination.id == combo_id).first()
        return self._to_schema(combo) if combo else None

    def get_all(self, size: int | None = None, occurred: bool | None = None) -> list[CombinationBase]:
        """Retrieve all Combinations with optional filters."""
        query = self.db.query(Combination)
        if size is not None:
            query = query.filter(Combination.size == size)
        if occurred is not None:
            query = query.filter(Combination.occurred == occurred)
        combos = query.order_by(Combination.size, Combination.id).all()
        return [self._to_schema(c) for c in combos]

    def toggle_occurred(self, combo_id: str) -> CombinationBase | None:
        """Toggle the occurred status of a combination."""
        combo = self.db.query(Combination).filter(Combination.id == combo_id).first()
        if not combo:
            return None
        combo.occurred = not combo.occurred
        combo.occurred_at = datetime.now() if combo.occurred else None
        self.db.commit()
        self.db.refresh(combo)
        return self._to_schema(combo)

    def mark_occurred(self, combo_id: str) -> tuple[CombinationBase, bool] | None:
        """Mark a combination as occurred. Returns (schema, was_already_occurred) or None."""
        combo = self.db.query(Combination).filter(Combination.id == combo_id).first()
        if not combo:
            return None
        was_already_occurred = combo.occurred
        combo.occurred = True
        combo.occurred_at = combo.occurred_at or datetime.now()
        self.db.commit()
        self.db.refresh(combo)
        return self._to_schema(combo), was_already_occurred

    def delete_all(self) -> int:
        """Delete all combinations. Returns count deleted."""
        count = self.db.query(Combination).count()
        self.db.query(Combination).delete()
        self.db.commit()
        return count

    @staticmethod
    def _to_schema(combo: Combination) -> CombinationBase:
        return CombinationBase(
            id=combo.id,
            size=combo.size,
            occurred=combo.occurred,
            occurred_at=combo.occurred_at,
            friends=[f.symbol for f in combo.friends],
        )
