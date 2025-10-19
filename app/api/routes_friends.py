"""Friends related API routes."""
from fastapi import APIRouter, HTTPException

from app.schemas.friend_schema import FriendBase, FriendUpdate
from app.services.friend_service import FriendService

router = APIRouter()
friend_service = FriendService()

# TODO:
#  - generic clean up of routes and consistency
#

@router.get("/friends", response_model=list[FriendBase])
def list_friends() -> list[FriendBase]:
    """List all Friends."""
    friends = friend_service.friend_repo.get_all()
    return friends


@router.get("/friends/{symbol}", response_model=FriendBase | None)
def get_friend(symbol: str) -> FriendBase | None:
    """Retrieve a Friend by symbol."""
    friend = friend_service.get_friend(symbol)
    if friend is None:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend


@router.post("/friends/", response_model=FriendBase | None)
def create_friend(friend: FriendBase) -> FriendBase | None:
    """Create a new Friend."""
    try:
        friend = friend_service.create_friend(
            symbol=friend.symbol,
            first_name=friend.first_name,
            last_name=friend.last_name
        )
        return friend
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/friends/{symbol}", response_model=dict)
def delete_friend(symbol: str) -> dict:
    """Delete a Friend by symbol."""
    try:
        result = friend_service.remove_friend(symbol)
        if not result:
            raise HTTPException(status_code=404, detail="Friend not found")
        return {"result": "Friend deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/friends/{symbol}", response_model=FriendBase | None)
def update_friend(symbol: str, friend_update: FriendUpdate) -> FriendBase | None:
    """Update an existing Friend's details."""
    try:
        friend = friend_service.modify_friend(
            symbol,
            friend_update.symbol,
            friend_update.first_name,
            friend_update.last_name
        )
        return friend
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
