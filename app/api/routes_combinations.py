"""Combination related API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.combination_schema import CombinationBase
from app.services.combination_service import CombinationService

router = APIRouter(prefix="/combinations", tags=["combinations"])


@router.get("", response_model=list[CombinationBase])
def list_combinations(
    size: int | None = None,
    occurred: bool | None = None,
    db: Session = Depends(get_db),
) -> list[CombinationBase]:
    """List all combinations with optional filters."""
    service = CombinationService(db)
    return service.get_all(size=size, occurred=occurred)


@router.get("/{combo_id}", response_model=CombinationBase)
def get_combination(combo_id: str, db: Session = Depends(get_db)) -> CombinationBase:
    """Get a single combination by ID."""
    service = CombinationService(db)
    combo = service.get_by_id(combo_id)
    if combo is None:
        raise HTTPException(status_code=404, detail="Combination not found")
    return combo


@router.patch("/{combo_id}/toggle", response_model=CombinationBase)
def toggle_combination(combo_id: str, db: Session = Depends(get_db)) -> CombinationBase:
    """Toggle the occurred status of a combination."""
    service = CombinationService(db)
    combo = service.toggle_occurred(combo_id)
    if combo is None:
        raise HTTPException(status_code=404, detail="Combination not found")
    return combo


@router.post("/regenerate", response_model=dict)
def regenerate_combinations(db: Session = Depends(get_db)) -> dict:
    """Regenerate all combinations from current friends."""
    service = CombinationService(db)
    count = service.regenerate_all()
    return {"result": f"Generated {count} combinations"}
