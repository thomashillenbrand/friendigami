"""Friends related API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.friend_schema import FriendBase
from app.services.friend_service import FriendService

router = APIRouter(prefix="/friends", tags=["friends"])


@router.get("", response_model=list[FriendBase])
def list_friends(db: Session = Depends(get_db)) -> list[FriendBase]:
    """List all Friends."""
    service = FriendService(db)
    return service.friend_repo.get_all()


@router.get("/{symbol}", response_model=FriendBase)
def get_friend(symbol: str, db: Session = Depends(get_db)) -> FriendBase:
    """Retrieve a Friend by symbol."""
    service = FriendService(db)
    friend = service.get_friend(symbol)
    if friend is None:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend


@router.post("", response_model=FriendBase)
def create_friend(friend: FriendBase, db: Session = Depends(get_db)) -> FriendBase:
    """Create a new Friend."""
    service = FriendService(db)
    try:
        return service.create_friend(
            symbol=friend.symbol,
            first_name=friend.first_name,
            last_name=friend.last_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{symbol}", response_model=dict)
def delete_friend(symbol: str, db: Session = Depends(get_db)) -> dict:
    """Delete a Friend by symbol."""
    service = FriendService(db)
    try:
        result = service.remove_friend(symbol)
        if not result:
            raise HTTPException(status_code=404, detail="Friend not found")
        return {"result": "Friend deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{symbol}", response_model=FriendBase)
def update_friend(symbol: str, friend_update: FriendBase, db: Session = Depends(get_db)) -> FriendBase:
    """Update an existing Friend's details."""
    service = FriendService(db)
    try:
        friend = service.modify_friend(
            symbol,
            friend_update.symbol,
            friend_update.first_name,
            friend_update.last_name,
        )
        if friend is None:
            raise HTTPException(status_code=404, detail="Friend not found")
        return friend
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
